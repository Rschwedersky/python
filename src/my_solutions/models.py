from django.db import models
from subscriptions.models import User

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login                   = models.CharField(max_length=150)
    password                = models.CharField(max_length=150)
    email_to_send_results   = models.CharField(max_length=150)
    encrypted_key           = models.CharField(max_length=1024)
    execution_interval      = models.IntegerField(default=0, null=False, blank=False)
    auto_run                = models.BooleanField(default=False)
    last_run                = models.DateTimeField(null=True, blank=True)
    last_status             = models.CharField(max_length=150)