from django.urls import path
from django.contrib.auth import views as auth_ciews   

from . import views


urlpatterns = [
    path("", views.notes_list, name="notes_list"),

    path("login/", auth_ciews.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_ciews.LogoutView.as_view(), name="logout"),
]