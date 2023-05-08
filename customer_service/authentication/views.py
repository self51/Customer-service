from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, CreateView, UpdateView,
                                  DetailView, ListView, )

from .models import User
from .services import ScheduleGenerate, credentials_to_dict
from .forms import (CustomerSignUpForm, WorkerSignUpForm,
                    WorkerUpdateForm, CustomerUpdateForm, )

import google_auth_oauthlib.flow


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class UserSettings(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/settings.html'
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('authentication:account')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        if self.request.user.is_customer:
            form = super().get_form(CustomerUpdateForm)
        else:
            form = super().get_form(WorkerUpdateForm)
        form.request = self.request
        return form


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
        data = super().get_context_data(**kwargs)
        worker = User.objects.get(pk=self.kwargs['pk'])
        day_str = self.request.GET.get('day', None)
        schedule = ScheduleGenerate(worker.id)
        schedule = ScheduleGenerate.define_day(worker.id, day_str) if day_str else schedule
        data['week'] = schedule.get_week()
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
        return User.objects.filter(is_worker=True).exclude(provide_service__exact='')


class CustomerDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'customer'
    template_name = 'user/customer_detail.html'
    redirect_field_name = reverse_lazy('login')

    def get_queryset(self):
        return User.objects.filter(is_customer=True)


class CustomerListView(ListView):
    context_object_name = 'customers'
    template_name = 'user/customers.html'

    def get_queryset(self):
        return User.objects.filter(is_customer=True)


def google_calendar_init(request):
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.CLIENT_SECRETS_FILE, scopes=settings.SCOPES)

    flow.redirect_uri = settings.REDIRECT_URL
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    request.session['state'] = state

    return HttpResponseRedirect(authorization_url)


def google_calendar_redirect(request):
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = request.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.CLIENT_SECRETS_FILE, scopes=settings.SCOPES, state=state)
    flow.redirect_uri = settings.REDIRECT_URL

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    # Save credentials to database
    credentials = credentials_to_dict(flow.credentials)
    user = User.objects.get(pk=request.user.id)
    user.set_google_calendar_credentials(credentials)

    return HttpResponseRedirect(reverse('authentication:account'))


def disable_google_calendar(request):
    # Deletes json with credentials form DB
    user = User.objects.get(pk=request.user.id)
    user.delete_google_calendar_credentials()
    return HttpResponseRedirect(reverse('authentication:account'))
