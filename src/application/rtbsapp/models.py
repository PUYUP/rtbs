from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.email


class Resturanttable(models.Model):
    tablenum = models.CharField(max_length=250)
    creationdate = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tablebooking(models.Model):
    bookingnumber = models.IntegerField(unique=True)
    fullname = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    phonenum = models.CharField(max_length=15, blank=True)  # Supports international formats
    bookingdate = models.DateField(default=timezone.now)
    noofguest = models.IntegerField(default=1)
    bookingtime = models.TimeField()
    postingdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250,blank=True)
    table_id = models.ForeignKey(Resturanttable, on_delete=models.CASCADE, null=True, blank=True, related_name='tablelocated')
    remark = models.CharField(max_length=250, blank=True)
    remark_date = models.DateTimeField(auto_now=True)
