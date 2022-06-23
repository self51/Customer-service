from django.db import models

from authentication.models import User


class Location(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30, blank=False)
    street = models.CharField(max_length=30, blank=False)
    house_number = models.CharField(max_length=30, blank=False)

class Schedule(models.Model):
    WEEKDAYS = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()