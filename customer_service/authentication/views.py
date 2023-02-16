from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, CreateView,
                                  DetailView, ListView,)

from .models import User
from worker.models import Schedule
from .forms import CustomerSignUpForm, WorkerSignUpForm

from .services import day_list_generate


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


class WorkerDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'worker'
    template_name = 'user/worker_detail.html'
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('appointment:booking')

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data()
        worker = User.objects.get(pk=self.kwargs['pk'])
        schedules = Schedule.objects.filter(worker=worker.id)
        data['day_list'] = day_list_generate(schedules)

        return data

    def get_queryset(self):
        return User.objects.filter(is_worker=True)

    @staticmethod
    def post(request, **kwargs):
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
