from django.urls import path

from .views import AppointmentCreateView, AppointmentListView


app_name = 'appointment'
urlpatterns = [
    path('booking/<int:pk>/', AppointmentCreateView.as_view(), name='booking'),
    path('appointments/<int:pk>/', AppointmentListView.as_view(), name='appointments'),
]
