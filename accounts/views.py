# accounts/views.py
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView, UpdateView
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.views import PasswordChangeView
from django.utils.timezone import now

from .forms import (
    CustomUserCreationForm, ProfileUpdateForm,
    CustomPasswordChangeForm
)
from .models import CustomUser
from .utils import send_activation_email
from events.models import Event   # event stats


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        participant_group, _ = Group.objects.get_or_create(name='Participant')
        user.groups.add(participant_group)
        send_activation_email(user, self.request)
        return super().form_valid(form)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except Exception:
            user = None
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')
        return render(request, 'accounts/activation_invalid.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # Profile info
        ctx['user'] = user

        # Events statistics
        ctx['stats'] = {
            'total': Event.objects.filter(organizer=user).count(),
            'upcoming': Event.objects.filter(organizer=user, start_time__gte=now()).count(),
            'past': Event.objects.filter(organizer=user, end_time__lt=now()).count(),
        }

        #  User-specific event list
        ctx['my_events'] = Event.objects.filter(organizer=user).order_by('-start_time')

        return ctx


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("accounts:profile")


def logout_view(request):
    logout(request)
    return redirect('home')
