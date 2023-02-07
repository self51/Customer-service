import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (TemplateView, CreateView,
                                  DetailView, ListView,)

from .models import User
from worker.models import Schedule
from .forms import CustomerSignUpForm, WorkerSignUpForm


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup_form_customer.html'


class WorkerSignUpView(CreateView):
    model = User
    form_class = WorkerSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup_form_worker.html'


def hour_list_generate(schedule):
    hour_list = []

    from_hour = schedule.from_hour
    to_hour = schedule.to_hour
    while from_hour <= to_hour:
        hour_list.append(from_hour.strftime('%H:%M'))
        from_hour = datetime.time(from_hour.hour + 1, from_hour.minute)

    return hour_list


def day_list_generate(schedules):
    day_list = []
    today = datetime.date.today()
    for next_day in range(7):
        day = {}
        current_day = today + datetime.timedelta(days=next_day)
        weekday = current_day.strftime("%A").upper()
        weekday_number = current_day.weekday()
        schedule = schedules.get(weekday=weekday_number)
        day["date"] = str(current_day)
        day["weekday"] = weekday
        day["hour_list"] = hour_list_generate(schedule)
        day_list.append(day)

    return day_list


class WorkerDetailView(DetailView):
    context_object_name = 'worker'
    template_name = 'user/worker_detail.html'
    success_url = reverse_lazy('appointment:booking')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data()
        worker = User.objects.get(pk=self.kwargs['pk'])
        schedules = Schedule.objects.filter(worker=worker.id)
        data['day_list'] = day_list_generate(schedules)

        return data

    def get_queryset(self):
        return User.objects.filter(is_worker=True)

    def post(self, request, *args, **kwargs):
        request.session['date_time'] = request.POST.get('date_time')
        return HttpResponseRedirect(reverse('appointment:booking', kwargs={'pk': kwargs['pk']}))


class WorkerListView(ListView):
    context_object_name = 'workers'
    model = User
    template_name = 'user/workers.html'

    def get_queryset(self):
        return User.objects.filter(is_worker=True)


class CustomerDetailView(DetailView):
    context_object_name = 'customer'
    template_name = 'user/customer_detail.html'

    def get_queryset(self):
        return User.objects.filter(is_customer=True)


class CustomerListView(ListView):
    context_object_name = 'customers'
    template_name = 'user/customers.html'

    def get_queryset(self):
        return User.objects.filter(is_customer=True)
