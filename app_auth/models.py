from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    Company_name = models.CharField(max_length=10,default='my_company')
    Company_address = models.TextField(max_length=50,default='my_company')
    Phone_number = models.CharField(max_length=10,default='my_company')
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
    Driver_Name = models.CharField(max_length=10)
    Vehicle_Number = models.CharField(max_length=10)
    Sim_Number = models.CharField(max_length=10)
    IMEI_Number = models.CharField(max_length=10)
    Device_Model = models.CharField(max_length=20, choices=CHOICES_1)
    Vehicle_Licence_No = models.CharField(max_length=10)
