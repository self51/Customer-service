from django import forms

from .models import Location, Schedule


class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Location
        fields = ('city', 'street', 'house_number')

    def save(self, commit=True):
        self.instance.worker = self.request.user
        return super().save(commit=commit)


class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Schedule
        fields = ('weekday', 'from_hour', 'to_hour')

    def save(self, commit=True):
        self.instance.worker = self.request.user
        return super().save(commit=commit)
