# accounts/urls.py
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import (
    SignUpView, ActivateAccountView, ProfileView,
    ProfileUpdateView, logout_view, CustomPasswordChangeView
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
      path("activation-sent/", TemplateView.as_view(template_name="accounts/activation_sent.html"), name="activation_sent"),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/change-password/', CustomPasswordChangeView.as_view(), name='change_password'),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    # Forgot Password Flow
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="email/password_reset_email.txt",
            html_email_template_name="email/password_reset_email.html",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
