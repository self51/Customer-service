from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import AppointmentForm
from authentication.models import User
from worker.models import Schedule
from .models import Appointment

from datetime import time


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment/booking.html'
    success_url = reverse_lazy('workers')

    def form_valid(self, form):
        form.instance.worker = User.objects.get(pk=self.kwargs['pk'])
        return super(AppointmentCreateView, self).form_valid(form)