from django.urls import path
from . import views

from .views import SignUpView, CustomerSignUpView, WorkerSignUpView


urlpatterns = [
    path('account/', views.account, name='account'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/customer/', CustomerSignUpView.as_view(), name='customer_signup'),
    path('signup/worker/', WorkerSignUpView.as_view(), name='worker_signup'),
]
