import datetime

from django.db import models
from django.core.validators import MinValueValidator

from authentication.models import User
from worker.models import Location, Schedule


class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workers')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='locations')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    time = models.TimeField()
    date = models.DateField(validators=[MinValueValidator(datetime.date.today)])
    status = models.BooleanField(default=False)

    def __str__(self):
        return 'Appointment for {}, {}, {}'.format(self.date, self.time, self.location)
