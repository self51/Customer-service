from django.db import models
from django.contrib.auth.models import AbstractUser

import allauth
from allauth.utils import get_request_param
from allauth.socialaccount.models import SocialLogin
from allauth.account.utils import get_next_redirect_url


@classmethod
def state_from_request(cls, request):
    state = {}
    next_url = get_next_redirect_url(request)
    try:
        request.session["user_type"] = get_request_param(request, "user", None)
    except KeyError:
        print('user_type not exist')

    if next_url:
        state["next"] = next_url
    state["process"] = get_request_param(request, "process", "login")
    state["scope"] = get_request_param(request, "scope", "")
    state["auth_params"] = get_request_param(request, "auth_params", "")

    return state


allauth.socialaccount.models.SocialLogin.state_from_request = state_from_request


class User(AbstractUser):
    is_customer = models.BooleanField('customer status', default=False)
    is_worker = models.BooleanField('worker status', default=False)
    provide_service = models.CharField(max_length=35, blank=False)
