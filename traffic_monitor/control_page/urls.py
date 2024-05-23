from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:id>/', views.edit, name='edit_task'),
    path('delete/<int:id>/', views.delete, name='delete_task'),
]