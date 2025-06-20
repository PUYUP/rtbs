from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True)

    def __str__(self):
        return self.email


class Resturanttable(models.Model):
    tablenum = models.CharField(max_length=250)
    creationdate = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tablenum


class Tablebooking(models.Model):
    bookingnumber = models.IntegerField(unique=True)
    fullname = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    phonenum = models.CharField(max_length=15, blank=True)  # Supports international formats
    bookingdate = models.DateField(default=timezone.now)
    noofguest = models.IntegerField(default=1)
    bookingtime = models.TimeField()
    postingdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250, blank=True)
    table_id = models.ForeignKey(
        Resturanttable,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tablelocated')
    remark = models.CharField(max_length=250, blank=True)
    remark_date = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '({}) - {}'.format(self.bookingnumber, self.fullname)


class TimeSlot(models.Model):
    class TypeofChoices(models.TextChoices):
        INCREMENT = 'increment', _('Increment')
        SESSION = 'session', _('Session')

    label = models.CharField(max_length=256)
    enabled = models.BooleanField(default=False)
    typeof = models.CharField(choices=TypeofChoices.choices, max_length=25)
    allow_reservation = models.BooleanField(default=True)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    increment_value = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.label
