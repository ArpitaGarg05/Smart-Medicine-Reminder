from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100, blank=True)

    # NEW (daily or weekly)
    frequency_type = models.CharField(
        max_length=10,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly')],
        default='daily'
    )

    # NEW (only for weekly)
    day_of_week = models.CharField(max_length=10, blank=True, null=True)

    total_quantity = models.PositiveIntegerField(default=1)
    remaining_quantity = models.PositiveIntegerField(default=1)
    start_date = models.DateField(auto_now_add=True)

    # AUTO calculate times per day
    @property
    def frequency_per_day(self):
        return self.schedules.count() or 1

    @property
    def days_left(self):
        if self.frequency_per_day <= 0:
            return 0
        return self.remaining_quantity / self.frequency_per_day

    @property
    def is_low_stock(self):
        return self.days_left <= 3

    @property
    def stock_percentage(self):
        if self.total_quantity == 0:
            return 0
        return int((self.remaining_quantity / self.total_quantity) * 100)

    def __str__(self):
        return self.name


# 🔥 ADD THIS NEW MODEL (IMPORTANT)
class MedicineSchedule(models.Model):
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    time = models.TimeField()

    #marked taken logic
    last_taken_date = models.DateField(null=True, blank=True)

    def is_taken_today(self):
        return self.last_taken_date == now().date()
    taken_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.medicine.name} at {self.time}"