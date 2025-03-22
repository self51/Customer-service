from __future__ import annotations

from typing import TYPE_CHECKING

from common.config.settings import APPOINTMENT_TIME_ZONE_KYIV
from common.custom_types.custom_types import Args, Kwargs, LocationID, WorkerID
from common.permissions.permissions import IsObjectOwner
from common.pydantic_models.location import LocationData
from common.pydantic_models.user import CustomerCredentialsModel
from core.appointment.models import AppointmentInputData
from dependency_injector.wiring import Provide, inject
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .forms import AppointmentForm
from .models import Appointment

if TYPE_CHECKING:
    from core.appointment.interfaces import CreateAppointmentUseCase
    from django.db.models import QuerySet


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment/booking.html'
    redirect_field_name = reverse_lazy('login')

    @inject
    def post(
        self,
        request: HttpRequest,
        create_appointment_u_c: CreateAppointmentUseCase = Provide[
            'create_appointment_u_c'
        ],
        *args: Args,
        **kwargs: Kwargs,
    ) -> HttpResponseRedirect | HttpResponseBadRequest:
        appointment_form = self.get_form()
        appointment_form.is_valid()
        if not (location := appointment_form.cleaned_data.get('location')):
            return HttpResponseBadRequest('Missing required parameter')
        create_appointment_u_c(
            appointment_input_data=AppointmentInputData(
                worker_id=WorkerID(int(self.kwargs['pk'])),
                location_data=LocationData(
                    location_id=LocationID(location.id), address=(str(location))
                ),
                date_time=self.request.session.pop('date_time'),
                customer_credentials=CustomerCredentialsModel.model_validate(
                    self.request.user
                ),
            ),
            time_zone=APPOINTMENT_TIME_ZONE_KYIV,
        )
        return HttpResponseRedirect(reverse_lazy('appointment:appointments'))


class AppointmentsListView(LoginRequiredMixin, ListView):
    model = Appointment
    context_object_name = 'appointments'
    redirect_field_name = reverse_lazy('login')

    def get_queryset(self) -> QuerySet[Appointment]:
        user = self.request.user
        if user.is_customer:
            return Appointment.objects.filter(customer=user)

        return Appointment.objects.filter(worker=user)


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    form_class = AppointmentForm
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('appointment:appointments')

    def get_object(self, queryset: QuerySet[Appointment] = None) -> Appointment:
        obj: Appointment = super().get_object(queryset)
        IsObjectOwner.ensure_customer_or_worker_access(self.request, obj)
        return obj
