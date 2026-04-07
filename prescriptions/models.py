from django.db import models
from django.contrib.auth.models import User


class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='prescriptions/')
    extracted_text = models.TextField(blank=True)
    ai_parsed_data = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
