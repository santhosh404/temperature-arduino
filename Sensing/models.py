from datetime import time
from django.db import models
from django.utils import timezone

class Table1(models.Model):
    reference_id = models.IntegerField(primary_key=True, default=0)
    api = models.CharField(max_length=16)


class Data(models.Model):
    api_key = models.ForeignKey(Table1, on_delete=models.CASCADE)
    temparature = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    dat = models.DateField(default=timezone.now)
    tim = models.TimeField(default= timezone.now)
