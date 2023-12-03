from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path("register/", user_views.register, name="user-register"),
    path("login/", auth_views.LoginView.as_view(template_name='users/user_login.html'), name="user-login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='users/user_logout.html'), name="user-logout"),
]