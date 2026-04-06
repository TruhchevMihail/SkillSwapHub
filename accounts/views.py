from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Avg, Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import AppUserCreateForm, AppUserProfileEditForm

UserModel = get_user_model()


class RegisterUserView(CreateView):
    form_class = AppUserCreateForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        role_name = form.cleaned_data.get('role')
        mentors_group, _ = Group.objects.get_or_create(name='Mentors')
        learners_group, _ = Group.objects.get_or_create(name='Learners')
        selected_group = mentors_group if role_name == 'Mentors' else learners_group
        self.object.groups.add(selected_group)

        login(self.request, self.object)
        messages.success(self.request, 'Your account is ready. Welcome to SkillSwap Hub!')
        return response


class SignInView(LoginView):
    template_name = 'accounts/login-page.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        return response


class SignOutView(LogoutView):
    next_page = reverse_lazy('home')


class ProfileDetailView(DetailView):
    model = UserModel
    template_name = 'accounts/profile-detail.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object

        rating_stats = profile_user.received_reviews.aggregate(
            avg_rating=Avg('rating'),
            reviews_count=Count('id'),
        )
        context['avg_rating'] = rating_stats['avg_rating']
        context['reviews_count'] = rating_stats['reviews_count']
        context['offers_count'] = profile_user.skill_offers.count()
        context['active_offers_count'] = profile_user.skill_offers.filter(is_active=True).count()
        context['bookings_as_learner_count'] = profile_user.bookings.count()
        context['written_reviews_count'] = profile_user.written_reviews.count()
        context['completed_sessions_as_mentor'] = profile_user.skill_offers.filter(bookings__status='Completed').distinct().count()
        context['recent_received_reviews'] = (
            profile_user.received_reviews
            .select_related('author', 'booking__offer')[:5]
        )
        context['recent_offers'] = (
            profile_user.skill_offers
            .select_related('category')
            .order_by('-created_at')[:4]
        )
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = AppUserProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Profile updated successfully.')
        return response

    def get_success_url(self):
        return reverse_lazy('profile-edit')


class ProfilePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password-change.html'
    success_url = reverse_lazy('profile-edit')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Password changed successfully.')
        return response


