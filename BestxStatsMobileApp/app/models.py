from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=30, blank=True)
    device_token = models.CharField(max_length=254, blank=True)