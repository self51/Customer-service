from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['location'].empty_label = 'Select'
        self.fields['time'] = forms.TimeField(widget=forms.Select(choices=kwargs['initial']['HOUR_CHOICES']))

    class Meta:
        model = Appointment
        fields = ('location', 'time')
