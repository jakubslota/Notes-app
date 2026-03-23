from django.urls import path
from django.contrib.auth import views as auth_views  
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.notes_list, name="notes_list"),

    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # NOTES Operations
    path('create/', views.note_create, name='note_create'),
    path('edit/<int:pk>/', views.note_edit, name='note_edit'),
    path('delete/<int:pk>/', views.note_delete, name='note_delete')
]