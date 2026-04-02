from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.activity import log_activity
from core.mixins import GroupRequiredMixin
from core.models import ActivityLog
from notifications.tasks import send_booking_reminder, send_review_reminder
from offers.models import SkillOffer
from .forms import BookingCreateForm, BookingStatusUpdateForm
from .models import Booking


class BookingCreateView(GroupRequiredMixin, CreateView):
    model = Booking
    form_class = BookingCreateForm
    template_name = 'bookings/booking-create.html'
    required_group_names = ('Learners',)

    def dispatch(self, request, *args, **kwargs):
        self.offer = get_object_or_404(SkillOffer, pk=self.kwargs['offer_pk'])

        if request.user.is_authenticated and not request.user.is_superuser and self.offer.owner == request.user:
            raise PermissionDenied('You cannot book your own offer.')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.offer = self.offer
        form.instance.learner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Your booking request was sent successfully.')
        log_activity(
            actor=self.request.user,
            action=ActivityLog.ACTION_BOOKING_CREATED,
            target_object=self.object,
            note=f'Booked offer: {self.offer.title}',
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offer'] = self.offer
        return context


class MyBookingsListView(GroupRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/my-bookings.html'
    context_object_name = 'bookings'
    required_group_names = ('Learners',)

    def get_queryset(self):
        return (
            Booking.objects
            .filter(learner=self.request.user)
            .select_related('offer', 'offer__owner', 'offer__category')
        )


class MentorBookingsListView(GroupRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/mentor-bookings.html'
    context_object_name = 'bookings'
    required_group_names = ('Mentors',)

    def get_queryset(self):
        return (
            Booking.objects
            .filter(offer__owner=self.request.user)
            .select_related('offer', 'learner', 'offer__category')
        )


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking-detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        queryset = Booking.objects.select_related('offer', 'learner', 'offer__owner', 'offer__category', 'review')
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(
            Q(learner=self.request.user) |
            Q(offer__owner=self.request.user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = getattr(self.object, 'review', None)
        context['review_obj'] = review
        context['can_leave_review'] = (
            self.request.user == self.object.learner
            and self.object.status == Booking.Status.COMPLETED
            and review is None
        )
        return context


class BookingStatusUpdateView(GroupRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingStatusUpdateForm
    template_name = 'bookings/booking-status-update.html'
    required_group_names = ('Mentors',)

    def get_queryset(self):
        queryset = Booking.objects.all()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(offer__owner=self.request.user)

    def form_valid(self, form):
        previous_status = self.object.status  # self.object already populated — no extra DB hit

        if previous_status == Booking.Status.CANCELLED:
            raise PermissionDenied('Cancelled bookings cannot be updated.')

        response = super().form_valid(form)
        new_status = self.object.status

        if previous_status != new_status:
            if new_status == Booking.Status.APPROVED:
                send_booking_reminder.delay(self.object.pk)

            if new_status == Booking.Status.COMPLETED:
                send_review_reminder.delay(self.object.pk)

        messages.success(self.request, 'Booking status updated successfully.')
        log_activity(
            actor=self.request.user,
            action=ActivityLog.ACTION_BOOKING_STATUS_CHANGED,
            target_object=self.object,
            note=f'Status {previous_status} -> {new_status}',
        )
        return response


class BookingCancelView(GroupRequiredMixin, View):
    required_group_names = ('Learners',)

    def post(self, request, pk):
        booking_lookup = {'pk': pk}
        if not request.user.is_superuser:
            booking_lookup['learner'] = request.user
        booking = get_object_or_404(Booking, **booking_lookup)

        if booking.status not in [Booking.Status.PENDING, Booking.Status.APPROVED]:
            raise PermissionDenied('Only pending or approved bookings can be cancelled.')

        booking.status = Booking.Status.CANCELLED
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')

        log_activity(
            actor=request.user,
            action=ActivityLog.ACTION_BOOKING_CANCELLED,
            target_object=booking,
        )

        return HttpResponseRedirect(reverse('booking-detail', kwargs={'pk': booking.pk}))





