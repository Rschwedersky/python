from django.conf import settings
from django.db import models


class Dashboard(models.Model):
    customer = models.ForeignKey(
        settings.CUSTOMER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DashboardSessionInfo(models.Model):
    session_start = models.DateTimeField(auto_now_add=False)
    session_end = models.DateTimeField(auto_now_add=False)
    session_duration = models.TimeField(auto_now_add=False)
    user_id = models.IntegerField(null=False, blank=False, default=0)
