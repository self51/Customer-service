from django.urls import path
from django.views.generic.base import TemplateView

from .views import (SignUpView, CustomerSignUpView, WorkerSignUpView,
                    WorkerListView, CustomerListView, WorkerDetailView,
                    CustomerDetailView,)


app_name = 'authentication'
urlpatterns = [
    path('account/', TemplateView.as_view(template_name='user/account.html'), name='account'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/customer/', CustomerSignUpView.as_view(), name='customer_signup'),
    path('signup/worker/', WorkerSignUpView.as_view(), name='worker_signup'),
    path('workers/', WorkerListView.as_view(), name='workers'),
    path('worker/<int:pk>/', WorkerDetailView.as_view(), name='worker_detail'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
]
