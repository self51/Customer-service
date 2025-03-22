from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms

from .models import Appointment

if TYPE_CHECKING:
    from common.custom_types.custom_types import Args, Kwargs


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args: Args, **kwargs: Kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['location'].empty_label = 'Select'

    class Meta:
        model = Appointment
        fields = ('location',)
