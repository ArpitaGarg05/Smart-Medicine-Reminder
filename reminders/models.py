from django.db import models
from django.contrib.auth.models import User

from medicines.models import Medicine


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    taken = models.BooleanField(default=False)

    class Meta:
        unique_together = ('medicine', 'time', 'date')
