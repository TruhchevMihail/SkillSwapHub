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


        context['top_mentors'] = (
            Review.objects.values('mentor__username')
            .annotate(avg_rating=Avg('rating'), reviews_count=Count('id'))
            .order_by('-avg_rating', '-reviews_count')[:5]
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
