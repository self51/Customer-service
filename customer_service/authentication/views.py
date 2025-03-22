from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import google_auth_oauthlib.flow
from common.custom_types.custom_types import WorkerID
from core.utils.google_utils import credentials_to_dict
from dependency_injector.wiring import Provide, inject
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import (
    CustomerSignUpForm,
    CustomerUpdateForm,
    WorkerSignUpForm,
    WorkerUpdateForm,
)
from .models import User

if TYPE_CHECKING:
    from common.custom_types.custom_types import Args, Kwargs
    from core.schedule.interfaces import RetrieveWorkerScheduleUseCase
    from django.db.models import QuerySet
    from django.forms import ModelForm


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'user/account.html'


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class UserSettings(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/settings.html'
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('authentication:account')

    def get_object(self, queryset: QuerySet[User] = None) -> User:
        user: User = self.request.user
        return user

    def get_form(
        self, form_class: ModelForm = None
    ) -> CustomerUpdateForm | WorkerUpdateForm:
        if self.request.user.is_customer:
            form: CustomerUpdateForm = super().get_form(CustomerUpdateForm)
        else:
            form: WorkerUpdateForm = super().get_form(WorkerUpdateForm)
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
    template_name = 'user/worker_detail.html'
    redirect_field_name = reverse_lazy('login')
    success_url = reverse_lazy('appointment:booking')

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_worker=True)

    @inject
    def get(
        self,
        request: HttpRequest,
        retrieve_worker_schedule_u_c: RetrieveWorkerScheduleUseCase = Provide[
            'retrieve_worker_schedule_u_c'
        ],
        *args: Args,
        **kwargs: Kwargs,
    ) -> HttpResponse:
        worker_id = WorkerID(int(self.kwargs['pk']))
        start_day_str = request.GET.get('day', None)
        start_day = (
            datetime.strptime(start_day_str, '%Y-%m-%d').date()
            if start_day_str
            else None
        )
        week_schedule = retrieve_worker_schedule_u_c(
            worker_id=worker_id,
            **({'start_day': start_day} if start_day else {}),  # type: ignore[arg-type]
        )
        context = {'worker': self.get_object(), 'week': week_schedule}
        return render(request, 'user/worker_detail.html', context)

    def post(self, request: HttpRequest, **kwargs: Kwargs) -> HttpResponseRedirect:
        request.session['date_time'] = request.POST.get('date_time')
        return HttpResponseRedirect(
            reverse('appointment:booking', kwargs={'pk': kwargs['pk']})
        )


class WorkerListView(ListView):
    context_object_name = 'workers'
    model = User
    template_name = 'user/workers.html'

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_worker=True).exclude(provide_service__exact='')


class CustomerDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'customer'
    template_name = 'user/customer_detail.html'
    redirect_field_name = reverse_lazy('login')

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_customer=True)


class CustomerListView(ListView):
    context_object_name = 'customers'
    template_name = 'user/customers.html'

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.filter(is_customer=True)


def google_calendar_init(request: HttpRequest) -> HttpResponseRedirect:
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow
    # steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.CLIENT_SECRETS_FILE, scopes=settings.SCOPES
    )

    flow.redirect_uri = settings.REDIRECT_URL
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server
        # apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true',
    )

    # Store the state so the callback can verify the auth server response.
    request.session['state'] = state

    return HttpResponseRedirect(authorization_url)


def google_calendar_redirect(request: HttpRequest) -> HttpResponseRedirect:
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = request.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.CLIENT_SECRETS_FILE, scopes=settings.SCOPES, state=state
    )
    flow.redirect_uri = settings.REDIRECT_URL

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    # Save credentials to database
    credentials = credentials_to_dict(flow.credentials)
    user = User.objects.get(pk=request.user.id)
    user.google_calendar_credentials = credentials
    user.save()

    return HttpResponseRedirect(reverse('authentication:account'))


def disconnect_google_calendar(request: HttpRequest) -> HttpResponseRedirect:
    # Deletes dict with credentials form DB
    user = User.objects.get(pk=request.user.id)
    user.google_calendar_credentials = None
    user.save()
    return HttpResponseRedirect(reverse('authentication:account'))
