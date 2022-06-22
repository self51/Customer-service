from django.urls import path, include
from .views import SignUpView, CustomerSignUpView, WorkerSignUpView


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/customer/', CustomerSignUpView.as_view(), name='customer_signup'),
    path('accounts/signup/worker/', WorkerSignUpView.as_view(), name='worker_signup'),
]