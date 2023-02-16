from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, ListView,
                                  DeleteView, )

from .forms import AppointmentForm
from .models import Appointment
from authentication.models import User


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment/booking.html'
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('authentication:workers')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

    def form_valid(self, form):
        if 'date_time' in self.request.session:
            date_time = self.request.session['date_time']
            date = date_time.split('/')[0]
            time = date_time.split('/')[1]
            self.request.session.pop('date_time')

            form.instance.worker = User.objects.get(pk=self.kwargs['pk'])
            form.instance.customer = self.request.user
            form.instance.date = date
            form.instance.time = time

            return super(AppointmentCreateView, self).form_valid(form)

        return HttpResponseRedirect(reverse_lazy('authentication:worker_detail', kwargs={'pk': self.kwargs['pk']}))


class AppointmentsListView(LoginRequiredMixin, ListView):
    model = Appointment
    context_object_name = 'appointments'
    template_name = 'appointments/appointment_list.html'
    redirect_field_name = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        if user.is_customer:
            return Appointment.objects.filter(customer=user)

        return Appointment.objects.filter(worker=user)


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    form_class = AppointmentForm
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('appointment:appointments')
