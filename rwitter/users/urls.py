from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path("register/", user_views.register, name="user-register"),
    path("login/", auth_views.LoginView.as_view(template_name='users/user_login.html'), name="user-login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='users/user_logout.html'), name="user-logout"),
    path("password-reset-request/", auth_views.PasswordResetView.as_view(template_name='users/password_reset_request.html'), name="password-reset"),
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_request_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_request_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_request_complete.html'), name="password_reset_complete"),
    path("profile/", user_views.profile, name="user-profile"),
]