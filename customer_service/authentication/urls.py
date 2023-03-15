from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from .views import (SignUpView, CustomerSignUpView, WorkerSignUpView,
                    WorkerListView, CustomerListView, WorkerDetailView,
                    CustomerDetailView, UserSettings, )


app_name = 'authentication'
urlpatterns = [
    path('account/', TemplateView.as_view(template_name='user/account.html'), name='account'),
    path('settings/<int:pk>/', UserSettings.as_view(), name='settings'),
    path('select/', SignUpView.as_view(), name='select_user'),
    path('signup/customer/', CustomerSignUpView.as_view(), name='customer_signup'),
    path('signup/worker/', WorkerSignUpView.as_view(), name='worker_signup'),
    path('workers/', WorkerListView.as_view(), name='workers'),
    path('worker/<int:pk>/', WorkerDetailView.as_view(), name='worker_detail'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('change-password/', auth_views.PasswordChangeView.as_view(
            template_name='user/change_password.html',
            success_url='/accounts/account'
        ),
        name='change_password'
    ),
]
