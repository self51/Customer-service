from django.urls import path
from .views import AppointmentCreateView


urlpatterns = [
    path('booking/<int:pk>/', AppointmentCreateView.as_view(), name='booking'),
]