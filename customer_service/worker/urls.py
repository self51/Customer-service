from django.urls import path

from .views import (LocationListView, ScheduleListView, ScheduleCreateView,
                    LocationCreateView, LocationUpdateView, ScheduleUpdateView,
                    LocationDeleteView, ScheduleDeleteView, )


app_name = 'worker'
urlpatterns = [
    path('location/', LocationListView.as_view(), name='locations'),
    path('location/add/', LocationCreateView.as_view(), name='location_add'),
    path('location/update/<int:pk>/', LocationUpdateView.as_view(), name='location_update'),
    path('location/delete/<int:pk>/', LocationDeleteView.as_view(), name='location_delete'),
    path('schedule/', ScheduleListView.as_view(), name='schedules'),
    path('schedule/add/', ScheduleCreateView.as_view(), name='schedule_add'),
    path('schedule/update/<int:pk>/', ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedule/delete/<int:pk>/', ScheduleDeleteView.as_view(), name='schedule_delete'),
]
