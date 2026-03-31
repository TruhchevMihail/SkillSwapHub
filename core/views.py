from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.views.generic import TemplateView

from bookings.models import Booking
from core.models import ActivityLog
from offers.models import SkillOffer
from reviews.models import Review


class HomePageView(TemplateView):
    template_name = 'core/home-page.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['my_offers_count'] = SkillOffer.objects.filter(owner=user).count()
        context['my_bookings_count'] = Booking.objects.filter(learner=user).count()
        context['mentor_bookings_count'] = Booking.objects.filter(offer__owner=user).count()
        context['my_reviews_count'] = Review.objects.filter(author=user).count()
        context['received_reviews_count'] = Review.objects.filter(mentor=user).count()
        context['mentor_avg_rating'] = Review.objects.filter(mentor=user).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']

        mentor_bookings = Booking.objects.filter(offer__owner=user)
        completed_as_mentor = mentor_bookings.filter(status=Booking.Status.COMPLETED).count()
        mentor_bookings_count = context['mentor_bookings_count']
        context['mentor_completion_rate'] = (
            (completed_as_mentor / mentor_bookings_count) * 100 if mentor_bookings_count else 0
        )

        responded_bookings = mentor_bookings.exclude(status=Booking.Status.PENDING)
        if responded_bookings.exists():
            total_hours = sum(
                (item.updated_at - item.created_at).total_seconds() / 3600
                for item in responded_bookings
            )
            context['avg_response_hours'] = total_hours / responded_bookings.count()
        else:
            context['avg_response_hours'] = None

        context['top_mentors'] = (
            Review.objects.values('mentor__username')
            .annotate(avg_rating=Avg('rating'), reviews_count=Count('id'))
            .order_by('-avg_rating')[:5]
        )

        context['recent_activity'] = ActivityLog.objects.filter(actor=user)[:8]

        context['recent_my_bookings'] = (
            Booking.objects.filter(learner=user)
            .select_related('offer', 'offer__category')[:5]
        )
        context['recent_mentor_bookings'] = (
            Booking.objects.filter(offer__owner=user)
            .select_related('offer', 'learner')[:5]
        )
        return context
