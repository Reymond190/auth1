from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    Company_name = models.CharField(max_length=10,default="Amigait technology")
    Company_address = models.CharField(max_length=50,default="Sholinganallur")
    Phone_number = models.CharField(max_length=10,default="9677691904")
    #
    # def __str__(self):
    #     return f'{self.user.username} Profile'

class DeviceManager(models.Manager):
    def get_by_id(self,id):
       qs = self.get_queryset().filter(id=id)
       if qs.count() == 1:
         return qs.first()
       return None

class AddDevice(models.Model):
    CHOICES_1 = (
        ('P', 'Prime 07'),
        ('B', 'Benley 140'),
        ('O', 'OBDII'),
        ('R', 'Optimus 2.0'),
    )
    CHOICES_2 = (
        ('A', 'Ambulance'),
        ('M', 'Motorcycle'),
        ('B', 'Bus'),
        ('C', 'Car'),
        ('M', 'Minivan'),
        ('T', 'Tempo'),
        ('T', 'Truck'),
    )
    User = settings.AUTH_USER_MODEL
    user = models.ForeignKey(User, null=True,on_delete=models.PROTECT)
    Driver_Name = models.CharField(max_length=10,null=True)
    Vehicle_Number = models.CharField(max_length=10,null=True)
    Vehile_Type = models.CharField(max_length=20,choices=CHOICES_2, null=True)
    Sim_Number = models.CharField(max_length=10,null=True)
    IMEI_Number = models.CharField(max_length=10,null=True)
    Device_Model = models.CharField(max_length=20, choices=CHOICES_1, null=True)
    Vehicle_Licence_No = models.CharField(max_length=10,null=True)

    objects = DeviceManager()

