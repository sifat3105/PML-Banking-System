from django.urls import path 
from . import views

urlpatterns = [
    path('create/', views.create_accounts, name='create_account'),
    path('login/', views.login_views, name='login_account'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
]
