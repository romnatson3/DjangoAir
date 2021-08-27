from django.contrib import admin
from .models import City, Option, SeatClass, Flight, Ticket, Airplane, Gate



@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_filter = ('name',)

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'airplane', 'destination', 'gate', 'datetime')


@admin.register(SeatClass)
class SeatClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name_passenger', 'lunch', 'luggage', 'flight',
                    'datetime', 'seat_class', 'total_price', 'passengers', 'gate',
                    'gateway_passed')
