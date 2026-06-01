from django.urls import path

from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance-list'),
    path('checkin/', views.attendance_checkin, name='attendance-checkin'),
    path('<int:pk>/', views.attendance_detail, name='attendance-detail'),
]
