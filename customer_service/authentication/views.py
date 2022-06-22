from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy


from .models import User
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
