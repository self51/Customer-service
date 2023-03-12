from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DeleteView,)

from .forms import LocationForm, ScheduleForm
from .models import Location, Schedule


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    context_object_name = 'locations'
    redirect_field_name = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        return Location.objects.filter(worker=user)


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    context_object_name = 'schedules'
    redirect_field_name = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        return Schedule.objects.filter(worker=user)


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'worker/location_form.html'
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('worker:locations')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'worker/schedule_form.html'
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('worker:schedules')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'worker/location_form.html'
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('worker:locations')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'worker/schedule_form.html'
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('worker:schedules')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    form_class = LocationForm
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('worker:locations')


class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule
    form_class = ScheduleForm
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('worker:schedules')
