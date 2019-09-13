from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class vehicle(models.Model):
    name = models.CharField(max_length=20,null=True)
    odometer = models.CharField(max_length=10, null=True)
    latitude = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=50, null=True)
    location = models.TextField(max_length=100,null=True)
    deviceImeiNo = models.CharField(max_length=15, null=True)
    plateNumber = models.CharField(max_length=10, null=True)
    AssetCode = models.CharField(max_length=10, null=True)
    speed = models.CharField(max_length=5, null=True)
    companyId = models.CharField(max_length=10, null=True)
    engine = models.CharField(max_length=50, null=True)
    assetId = models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=10, null=True)
    direction = models.CharField(max_length=10, null=True)