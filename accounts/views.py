from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import AppUserCreateForm


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
