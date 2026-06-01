from django.urls import path

from . import views

urlpatterns = [
    path('', views.event_list_create, name='event-list'),
    path('<int:pk>/', views.event_detail, name='event-detail'),
    path('<int:pk>/status/', views.event_change_status, name='event-change-status'),
]
