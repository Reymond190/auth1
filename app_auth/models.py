from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    Company_name = models.CharField(max_length=10)
    Company_address = models.CharField(max_length=50)
    Phone_number = models.CharField(max_length=10)
    #
    # def __str__(self):
    #     return f'{self.user.username} Profile'

class AddDevice(models.Model):
    CHOICES_1 = (
        ('P', 'Prime 07'),
        ('B', 'Benley 140'),
        ('O', 'OBDII'),
        ('R', 'Optimus 2.0'),

    )
    Driver_Name = models.CharField(max_length=10,null=True)
    Vehicle_Number = models.CharField(max_length=10,null=True)
    Sim_Number = models.CharField(max_length=10,null=True)
    IMEI_Number = models.CharField(max_length=10,null=True)
    Device_Model = models.CharField(max_length=20, choices=CHOICES_1,null=True)
    Vehicle_Licence_No = models.CharField(max_length=10,null=True)
