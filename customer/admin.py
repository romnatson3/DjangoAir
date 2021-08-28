from django.contrib import admin
from .models import City, Option, SeatClass, Flight, Ticket, Airplane, Gate, SeatNumber



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


@admin.register(SeatNumber)
class SeatNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'airplane', 'seat_class', 'number')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'lunch', 'luggage', 'flight',
                    'datetime', 'seat_class', 'total_price', 'gate', 'seat',
                    'gateway_passed', 'ticket_code', 'create_datetime')
