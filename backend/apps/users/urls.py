from django.urls import path

from . import views

auth_urlpatterns = [
    path('register/', views.register_view, name='auth-register'),
    path('login/', views.login_view, name='auth-login'),
    path('logout/', views.logout_view, name='auth-logout'),
    path('refresh/', views.refresh_view, name='auth-refresh'),
    path('forgot-password/', views.forgot_password_view, name='auth-forgot-password'),
    path('change-password/', views.change_password_view, name='auth-change-password'),
    path('verify-email/', views.verify_email_view, name='auth-verify-email'),
    path('resend-verification/', views.resend_verification_view, name='auth-resend-verification'),
    path('reset-password/', views.reset_password_view, name='auth-reset-password'),
]

user_urlpatterns = [
    path('profile/', views.profile_view, name='user-profile'),
    path('', views.user_list_view, name='user-list'),
    path('<int:user_id>/', views.user_detail_view, name='user-detail'),
]
