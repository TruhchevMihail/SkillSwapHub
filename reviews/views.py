from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from bookings.models import Booking
from core.activity import log_activity
from core.mixins import GroupRequiredMixin
from core.models import ActivityLog
from .forms import ReviewCreateForm, ReviewEditForm
from .models import Review


class ReviewCreateView(GroupRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'reviews/review-create.html'
    required_group_names = ('Learners',)

    def dispatch(self, request, *args, **kwargs):
        self.booking = get_object_or_404(Booking, pk=self.kwargs['booking_pk'])

        if request.user.is_authenticated and not request.user.is_superuser:
            if self.booking.learner != request.user:
                raise PermissionDenied('Only the learner can review this booking.')

            if self.booking.status != Booking.Status.COMPLETED:
                raise PermissionDenied('You can only review completed bookings.')

            if hasattr(self.booking, 'review'):
                raise PermissionDenied('This booking already has a review.')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.booking = self.booking
        form.instance.author = self.booking.learner if self.request.user.is_superuser else self.request.user
        form.instance.mentor = self.booking.offer.owner
        response = super().form_valid(form)
        messages.success(self.request, 'Thanks for sharing your review.')
        log_activity(
            actor=self.request.user,
            action=ActivityLog.ACTION_REVIEW_CREATED,
            target_object=self.object,
            note=f'Reviewed mentor: {self.object.mentor.username}',
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = self.booking
        return context


class ReviewUpdateView(GroupRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewEditForm
    template_name = 'reviews/review-edit.html'
    required_group_names = ('Learners',)

    def get_queryset(self):
        queryset = Review.objects.select_related(
            'booking', 'booking__offer', 'mentor',
        )
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your review was updated.')
        log_activity(
            actor=self.request.user,
            action=ActivityLog.ACTION_REVIEW_UPDATED,
            target_object=self.object,
        )
        return response


class ReviewDeleteView(GroupRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review-delete.html'
    required_group_names = ('Learners',)

    def get_queryset(self):
        queryset = Review.objects.all()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        mentor_name = self.object.mentor.username
        log_activity(
            actor=request.user,
            action=ActivityLog.ACTION_REVIEW_DELETED,
            target_object=self.object,
        )
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Your review for {mentor_name} was deleted.')
        return response

    def get_success_url(self):
        return reverse_lazy('offer-detail', kwargs={'pk': self.object.booking.offer.pk})




