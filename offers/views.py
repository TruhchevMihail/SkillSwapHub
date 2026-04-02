from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.activity import log_activity
from core.mixins import GroupRequiredMixin, UserFilteredQuerysetMixin
from core.models import ActivityLog
from .forms import SkillOfferCreateForm, SkillOfferEditForm, SkillOfferFilterForm
from .models import FavoriteList, SkillOffer


class OfferListView(ListView):
    model = SkillOffer
    template_name = 'offers/offer-list.html'
    context_object_name = 'offers'
    paginate_by = 6

    def get_queryset(self):
        queryset = SkillOffer.objects.filter(is_active=True).select_related('owner', 'category').prefetch_related('tags')

        self.filter_form = SkillOfferFilterForm(self.request.GET)

        if self.filter_form.is_valid():
            search = self.filter_form.cleaned_data.get('search')
            category = self.filter_form.cleaned_data.get('category')
            level = self.filter_form.cleaned_data.get('level')
            max_price = self.filter_form.cleaned_data.get('max_price')
            sort_by = self.filter_form.cleaned_data.get('sort_by')

            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search)
                )

            if category:
                queryset = queryset.filter(category=category)

            if level:
                queryset = queryset.filter(level=level)

            if max_price is not None:
                queryset = queryset.filter(price_per_session__lte=max_price)

            if sort_by == 'oldest':
                queryset = queryset.order_by('created_at')
            elif sort_by == 'price_asc':
                queryset = queryset.order_by('price_per_session')
            elif sort_by == 'price_desc':
                queryset = queryset.order_by('-price_per_session')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context


class OfferDetailView(DetailView):
    model = SkillOffer
    template_name = 'offers/offer-detail.html'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = (
            self.object.bookings
            .filter(status='Completed', review__isnull=False)
            .select_related('review', 'review__author')
        )
        mentor_rating_stats = self.object.owner.received_reviews.aggregate(
            avg_rating=Avg('rating'),
            reviews_count=Count('id'),
        )
        context['mentor_avg_rating'] = mentor_rating_stats['avg_rating']
        context['mentor_reviews_count'] = mentor_rating_stats['reviews_count']

        is_favorite = False
        if self.request.user.is_authenticated:
            favorite_list, _ = FavoriteList.objects.get_or_create(user=self.request.user)
            is_favorite = favorite_list.offers.filter(pk=self.object.pk).exists()

        context['is_favorite'] = is_favorite
        return context


class OfferCreateView(GroupRequiredMixin, CreateView):
    model = SkillOffer
    form_class = SkillOfferCreateForm
    template_name = 'offers/offer-create.html'
    required_group_names = ('Mentors',)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Your offer is now live.')
        log_activity(
            actor=self.request.user,
            action=ActivityLog.ACTION_OFFER_CREATED,
            target_object=self.object,
        )
        return response


class OfferUpdateView(GroupRequiredMixin, UserFilteredQuerysetMixin, UpdateView):
    model = SkillOffer
    form_class = SkillOfferEditForm
    template_name = 'offers/offer-edit.html'
    required_group_names = ('Mentors',)
    user_lookup = 'owner'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Offer details updated successfully.')
        log_activity(
            actor=self.request.user,
            action=ActivityLog.ACTION_OFFER_UPDATED,
            target_object=self.object,
        )
        return response


class OfferDeleteView(GroupRequiredMixin, UserFilteredQuerysetMixin, DeleteView):
    model = SkillOffer
    template_name = 'offers/offer-delete.html'
    success_url = reverse_lazy('offer-list')
    required_group_names = ('Mentors',)
    user_lookup = 'owner'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        offer_title = self.object.title
        log_activity(
            actor=request.user,
            action=ActivityLog.ACTION_OFFER_DELETED,
            target_object=self.object,
            note=f'Deleted offer: {self.object}',
        )
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Offer “{offer_title}” was deleted.')
        return response


class MyOffersListView(GroupRequiredMixin, ListView):
    model = SkillOffer
    template_name = 'offers/my-offers.html'
    context_object_name = 'offers'
    required_group_names = ('Mentors',)

    def get_queryset(self):
        return (
            SkillOffer.objects
            .filter(owner=self.request.user)
            .select_related('category')
            .prefetch_related('tags')
        )


class FavoriteOffersListView(GroupRequiredMixin, ListView):
    model = SkillOffer
    template_name = 'offers/favorites.html'
    context_object_name = 'offers'
    required_group_names = ('Learners',)

    def get_queryset(self):
        favorite_list, _ = FavoriteList.objects.get_or_create(user=self.request.user)
        return favorite_list.offers.all().select_related('owner', 'category').prefetch_related('tags')


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_superuser and not request.user.groups.filter(name='Learners').exists():
            messages.warning(request, 'Only learners can save offers to favourites.')
            return HttpResponseRedirect(reverse_lazy('offer-list'))

        offer = get_object_or_404(SkillOffer, pk=pk)
        favorite_list, _ = FavoriteList.objects.get_or_create(user=request.user)

        if offer in favorite_list.offers.all():
            favorite_list.offers.remove(offer)
            messages.info(request, 'Offer removed from your saved list.')
        else:
            favorite_list.offers.add(offer)
            messages.success(request, 'Offer added to your saved list.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('offer-list')))
