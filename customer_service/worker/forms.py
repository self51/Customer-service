from django import forms

from .models import Location, Schedule


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('city', 'street', 'house_number')

    def save(self, commit: bool = True) -> Location:
        self.instance.worker = self.request.user
        location: Location = super().save(commit=commit)
        return location


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('weekday', 'from_hour', 'to_hour')

    def save(self, commit: bool = True) -> Schedule:
        self.instance.worker = self.request.user
        schedule: Schedule = super().save(commit=commit)
        return schedule
