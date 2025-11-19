# labelmanager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.valid_labels, name='valid_labels'),
    path('edit/<int:pk>/', views.edit_label, name='edit_label'),
    path('remove/<int:pk>/', views.remove_label, name='remove_label'),
]
