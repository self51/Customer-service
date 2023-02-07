from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['location'].empty_label = 'Select'

    class Meta:
        model = Appointment
        fields = ('location', )
