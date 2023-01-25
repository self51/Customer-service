from django.db import models

from authentication.models import User
from worker.models import Location, Schedule

WEEKDAYS_CHOICES = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
)


class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workers')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='locations')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    time = models.TimeField()
    weekday = models.IntegerField(choices=WEEKDAYS_CHOICES)
    status = models.BooleanField(default=False)
