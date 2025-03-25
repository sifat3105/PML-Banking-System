from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('account/details', views.account_details, name='account_details'),
    path('deposit/', views.account_deposit, name='deposit'),
    path('withdraw/', views.account_withdraw, name='withdraw'),
    path('transfer/', views.account_transfer, name='transfer'),
    path('transactions/', views.account_transactions, name='transactions'),
    
]
