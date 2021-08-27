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

    def __str__(self):
        return f'{self.id}, {self.name}, {self.country}'



class SeatClass(models.Model):

    class Meta():
        verbose_name = 'seat_class'

    name = models.CharField(max_length=256)
    price = models.FloatField(default=0.00)

    def __str__(self):
        return f'{self.name}, {self.price}'



class Option(models.Model):

    class Meta():
        verbose_name = 'option'

    name = models.CharField(max_length=256)
    price = models.FloatField(default=0.00)

    def __str__(self):
        return f'{self.name}'



class Airplane(models.Model):

    class Meta():
        verbose_name = 'airplane'

    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'



class Gate(models.Model):

    class Meta():
        verbose_name = 'gate'

    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'



class Flight(models.Model):

    class Meta():
        verbose_name = 'flight'

    airplane = models.ForeignKey(Airplane, on_delete=models.PROTECT)
    destination = models.ForeignKey(City, on_delete=models.PROTECT)
    gate = models.ForeignKey(Gate, on_delete=models.PROTECT)
    datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.id}'



class Ticket(models.Model):

    class Meta():
        verbose_name = 'ticket'

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name_passenger = models.CharField(max_length=256)
    passengers = models.IntegerField(blank=False)
    datetime = models.DateTimeField()
    seat_class = models.ForeignKey(SeatClass, on_delete=models.PROTECT, db_column='seat_class')
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    gate = models.ForeignKey(Gate, on_delete=models.PROTECT)
    total_price = models.FloatField(default=0.00)
    lunch = models.BooleanField(default=False)
    luggage = models.BooleanField(default=False)
    gateway_passed = models.BooleanField(default=False)
