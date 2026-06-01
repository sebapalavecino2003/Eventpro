from django.urls import path

from . import views

urlpatterns = [
    path('', views.invitation_list_create, name='invitation-list'),
    path('<int:pk>/', views.invitation_detail, name='invitation-detail'),
    path('<int:pk>/rsvp/', views.invitation_rsvp, name='invitation-rsvp'),
]
