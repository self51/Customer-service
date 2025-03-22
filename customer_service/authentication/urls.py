from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import (
    AccountView,
    CustomerDetailView,
    CustomerListView,
    CustomerSignUpView,
    SignUpView,
    UserSettings,
    WorkerDetailView,
    WorkerListView,
    WorkerSignUpView,
)

app_name = 'authentication'
urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),
    path('settings/', UserSettings.as_view(), name='settings'),
    path('select/', SignUpView.as_view(), name='select_user'),
    path('signup/customer/', CustomerSignUpView.as_view(), name='customer_signup'),
    path('signup/worker/', WorkerSignUpView.as_view(), name='worker_signup'),
    path('workers/', WorkerListView.as_view(), name='workers'),
    path('worker/<int:pk>/', WorkerDetailView.as_view(), name='worker_detail'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='user/change_password.html', success_url='/accounts/account'
        ),
        name='change_password',
    ),
    path('google/calendar/init/', views.google_calendar_init, name='google_permission'),
    path(
        'google/login/callback/calendar/',
        views.google_calendar_redirect,
        name='google_redirect',
    ),
    path(
        'google/calendar/disconnect',
        views.disconnect_google_calendar,
        name='disconnect_google_calendar',
    ),
]
