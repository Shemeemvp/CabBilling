from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    full_name = models.CharField(max_length = 150, null = True, blank = True)
    mobile = models.BigIntegerField(null = True, blank = True)

class TSC_Form(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    driver = models.ForeignKey(Driver, on_delete = models.SET_NULL, null = True)
    trip_no = models.CharField(max_length = 50, null = True, blank = True)
    trip_date = models.DateField(null = True, blank = True)
    driver_name = models.CharField(max_length = 150, null = True, blank = True)
    guest = models.CharField(max_length = 150, null = True, blank = True)
    vehicle_no = models.CharField(max_length = 50, null = True, blank = True)
    starting_place = models.CharField(max_length = 150, null = True, blank = True)
    starting_time = models.TimeField(null = True, blank = True)
    destination = models.CharField(max_length = 150, null = True, blank = True)
    time_of_arrival = models.TimeField(null = True, blank = True)
    kilometers = models.FloatField(default = 0.0, null = True, blank = True)
    toll = models.FloatField(default = 0.0, null = True, blank = True)
    parking = models.FloatField(default = 0.0, null = True, blank = True)
    entrance = models.FloatField(default = 0.0, null = True, blank = True)
    guide_fee = models.FloatField(default = 0.0, null = True, blank = True)
    advance = models.FloatField(default = 0.0, null = True, blank = True)
    debit = models.FloatField(default = 0.0, null = True, blank = True)
    balance = models.FloatField(default = 0.0, null = True, blank = True)
    bill_qr = models.CharField(max_length=500, default='',null=True,blank=True)

class Customer_Feedbacks(models.Model):
    full_name = models.CharField(max_length = 150, null = True, blank = True)
    feedback = models.TextField()