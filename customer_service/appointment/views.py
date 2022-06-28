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

    def get_initial(self):
        initial = super().get_initial()
        worker = User.objects.get(pk=self.kwargs['pk'])
        schedule = Schedule.objects.get(id=worker.id)
        HOUR_CHOICES = []
        from_hour = schedule.from_hour
        to_hour = schedule.to_hour
        while from_hour <= to_hour:
            HOUR_CHOICES.append(from_hour)
            from_hour = time(from_hour.hour + 1, from_hour.minute)

        HOUR_CHOICES = sorted([(valid_time, valid_time.strftime('%H:%M')) for valid_time in HOUR_CHOICES],key=lambda x: x[0])

        initial['HOUR_CHOICES'] = HOUR_CHOICES

        return initial

    def form_valid(self, form):
        form.instance.worker = User.objects.get(pk=self.kwargs['pk'])
        return super(AppointmentCreateView, self).form_valid(form)