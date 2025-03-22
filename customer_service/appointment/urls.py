from django.urls import path

from .views import AppointmentCreateView, AppointmentDeleteView, AppointmentsListView

app_name = 'appointment'
urlpatterns = [
    path('booking/<int:pk>/', AppointmentCreateView.as_view(), name='booking'),
    path('appointments/', AppointmentsListView.as_view(), name='appointments'),
    path(
        'appointments/delete/<int:pk>/',
        AppointmentDeleteView.as_view(),
        name='appointments-delete',
    ),
]
