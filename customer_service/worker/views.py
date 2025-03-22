from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LocationForm, ScheduleForm
from .models import Location, Schedule

if TYPE_CHECKING:
    from django.db.models import QuerySet


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    context_object_name = 'locations'
    redirect_field_name = 'login'

    def get_queryset(self) -> QuerySet[Location]:
        return Location.objects.filter(worker=self.request.user)


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'worker/location_form.html'
    success_url = reverse_lazy('worker:locations')

    def get_form(self, form_class: LocationForm | None = None) -> LocationForm:
        form: LocationForm = super().get_form(form_class)
        form.request = self.request
        return form


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'worker/location_form.html'
    success_url = reverse_lazy('worker:locations')

    def get_form(self, form_class: LocationForm | None = None) -> LocationForm:
        form: LocationForm = super().get_form(form_class)
        form.request = self.request
        return form


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('worker:locations')


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'worker/schedule_form.html'
    success_url = reverse_lazy('worker:schedules')

    def get_form(self, form_class: ScheduleForm | None = None) -> ScheduleForm:
        form: ScheduleForm = super().get_form(form_class)
        form.request = self.request
        return form


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    context_object_name = 'schedules'
    redirect_field_name = 'login'

    def get_queryset(self) -> QuerySet[Schedule]:
        return Schedule.objects.filter(worker=self.request.user)


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'worker/schedule_form.html'
    success_url = reverse_lazy('worker:schedules')

    def get_form(self, form_class: ScheduleForm | None = None) -> ScheduleForm:
        form: ScheduleForm = super().get_form(form_class)
        form.request = self.request
        return form


class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule
    success_url = reverse_lazy('worker:schedules')
