from django.contrib.auth.models import User
from django.db import models


class City(models.Model):

    class Meta():
        verbose_name = 'city'
        indexes = [
           models.Index(fields=['name']),
        ]

    name = models.CharField(max_length=256, blank=False)
    country = models.CharField(max_length=256, blank=False)



class SeatClass(models.Model):

    class Meta():
        verbose_name = 'seat_class'

    name = models.CharField(max_length=256)
    price = models.FloatField(default=0.00)



class Option(models.Model):

    class Meta():
        verbose_name = 'option'

    name = models.CharField(max_length=256)
    price = models.FloatField(default=0.00)
