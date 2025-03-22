from authentication.models import User
from django.db import models

WEEKDAYS_CHOICES = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class Location(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30, blank=False)
    street = models.CharField(max_length=30, blank=False)
    house_number = models.CharField(max_length=30, blank=False)

    def __str__(self) -> str:
        return f'{self.city}, {self.street}, {self.house_number}'


class Schedule(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS_CHOICES)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self) -> str:
        return f'Time slot on {self.get_weekday_display()} from {self.from_hour} to {self.to_hour}'
