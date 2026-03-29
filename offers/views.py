"""Views for creating, browsing, and managing offers."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import SkillOfferCreateForm, SkillOfferEditForm, SkillOfferFilterForm
from .models import FavoriteList, SkillOffer


class OfferListView(ListView):
    """Display all active skill offers with filtering and sorting options."""
    
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
    """Display details of a single skill offer."""
    
    model = SkillOffer
    template_name = 'offers/offer-detail.html'
    context_object_name = 'offer'


class OfferCreateView(LoginRequiredMixin, CreateView):
    """Create a new skill offer."""
    
    model = SkillOffer
    form_class = SkillOfferCreateForm
    template_name = 'offers/offer-create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OfferUpdateView(LoginRequiredMixin, UpdateView):
    """Edit an existing skill offer (owner only)."""
    
    model = SkillOffer
    form_class = SkillOfferEditForm
    template_name = 'offers/offer-edit.html'

    def get_queryset(self):
        return SkillOffer.objects.filter(owner=self.request.user)


class OfferDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a skill offer (owner only) with confirmation."""
    
    model = SkillOffer
    template_name = 'offers/offer-delete.html'
    success_url = reverse_lazy('offer-list')

    def get_queryset(self):
        return SkillOffer.objects.filter(owner=self.request.user)


class MyOffersListView(LoginRequiredMixin, ListView):
    """Display all offers created by the current user."""
    
    model = SkillOffer
    template_name = 'offers/my-offers.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return SkillOffer.objects.filter(owner=self.request.user).select_related('category').prefetch_related('tags')


class FavoriteOffersListView(LoginRequiredMixin, ListView):
    """Display all offers in the user's favorite list."""
    
    model = SkillOffer
    template_name = 'offers/favorites.html'
    context_object_name = 'offers'

    def get_queryset(self):
        favorite_list, _ = FavoriteList.objects.get_or_create(user=self.request.user)
        return favorite_list.offers.all().select_related('owner', 'category').prefetch_related('tags')


class ToggleFavoriteView(LoginRequiredMixin, View):
    """Add or remove a skill offer from the user's favorite list."""
    
    def post(self, request, pk):
        offer = get_object_or_404(SkillOffer, pk=pk)
        favorite_list, _ = FavoriteList.objects.get_or_create(user=request.user)

        if offer in favorite_list.offers.all():
            favorite_list.offers.remove(offer)
        else:
            favorite_list.offers.add(offer)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('offer-list')))


