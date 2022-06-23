from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Location, Schedule
from .forms import LocationForm, ScheduleForm


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
    success_url = reverse_lazy('locations')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'worker/schedule_form.html'
    success_url = reverse_lazy('schedules')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'worker/location_form.html'
    success_url = reverse_lazy('locations')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'worker/schedule_form.html'
    success_url = reverse_lazy('schedules')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

class LocationDeleteView(DeleteView):
    model = Location
    form_class = LocationForm
    success_url = reverse_lazy('locations')

class ScheduleDeleteView(DeleteView):
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('schedules')