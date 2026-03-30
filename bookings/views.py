from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from offers.models import SkillOffer
from .forms import BookingCreateForm, BookingStatusUpdateForm
from .models import Booking


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingCreateForm
    template_name = 'bookings/booking-create.html'

    def dispatch(self, request, *args, **kwargs):
        self.offer = get_object_or_404(SkillOffer, pk=self.kwargs['offer_pk'])

        if request.user.is_authenticated and self.offer.owner == request.user:
            raise PermissionDenied('You cannot book your own offer.')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.offer = self.offer
        form.instance.learner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offer'] = self.offer
        return context


class MyBookingsListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/my-bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(
            learner=self.request.user
        ).select_related('offer', 'offer__owner', 'offer__category')


class MentorBookingsListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/mentor-bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(
            offer__owner=self.request.user
        ).select_related('offer', 'learner', 'offer__category')


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking-detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.filter(
            Q(learner=self.request.user) |
            Q(offer__owner=self.request.user)
        ).select_related('offer', 'learner', 'offer__owner', 'offer__category')


class BookingStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingStatusUpdateForm
    template_name = 'bookings/booking-status-update.html'

    def get_queryset(self):
        return Booking.objects.filter(offer__owner=self.request.user)

    def form_valid(self, form):
        booking = form.instance

        if booking.status == Booking.Status.CANCELLED:
            raise PermissionDenied('Cancelled bookings cannot be updated.')

        return super().form_valid(form)


class BookingCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(
            Booking,
            pk=pk,
            learner=request.user,
        )

        if booking.status not in [Booking.Status.PENDING, Booking.Status.APPROVED]:
            raise PermissionDenied('Only pending or approved bookings can be cancelled.')

        booking.status = Booking.Status.CANCELLED
        booking.save()

        return HttpResponseRedirect(reverse('booking-detail', kwargs={'pk': booking.pk}))




