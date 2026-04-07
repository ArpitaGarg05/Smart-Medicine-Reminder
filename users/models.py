from django.db import models
from django.contrib.auth.models import User


class CaregiverAccess(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caregiver_accesses')
    caregiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_owner_accesses')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'caregiver')
        ordering = ['-created_at']
