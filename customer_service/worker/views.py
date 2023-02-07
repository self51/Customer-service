from django.urls import reverse_lazy
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView,)

from .forms import LocationForm, ScheduleForm
from .models import Location, Schedule


class LocationListView(ListView):
    context_object_name = 'locations'
    model = Location


class ScheduleListView(ListView):
    context_object_name = 'schedules'
    model = Schedule


class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'worker/location_form.html'
    success_url = reverse_lazy('worker:locations')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'worker/schedule_form.html'
    success_url = reverse_lazy('worker:schedules')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'worker/location_form.html'
    success_url = reverse_lazy('worker:locations')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'worker/schedule_form.html'
    success_url = reverse_lazy('worker:schedules')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


class LocationDeleteView(DeleteView):
    model = Location
    form_class = LocationForm
    success_url = reverse_lazy('worker:locations')


class ScheduleDeleteView(DeleteView):
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('worker:schedules')
