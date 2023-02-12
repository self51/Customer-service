from django.urls import path

from .views import (AppointmentCreateView, AppointmentsListView,
                    AppointmentDeleteView,)


app_name = 'appointment'
urlpatterns = [
    path('booking/<int:pk>/', AppointmentCreateView.as_view(), name='booking'),
    path('appointments/', AppointmentsListView.as_view(), name='appointments'),
    path('appointments/delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment_delete'),
]
