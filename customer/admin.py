from django.contrib import admin
from .models import City, Option, SeatClass, Flight, Ticket, Airplane, Gate, SeatNumber


admin.site.site_title = 'GgangoAir'
admin.site.site_header = 'GgangoAir'


class FlightInline(admin.TabularInline):
    model = Flight
    extra = 1
    readonly_fields = ('datetime',)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'airplane', 'destination', 'gate', 'datetime')
    list_filter = ('airplane',)
    list_display_links = ('destination',)
    fieldsets = (
        (
            'Gate_Airplane', {
                'fields': (('gate', 'airplane'),)
            }
        ),
        (
            'Destination', {
                'classes': ('collapse',), 'fields': (('destination', 'datetime'),)
            }
        ),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    inlines = [FlightInline]
    search_fields = ['name']
    list_display_links = ('name',)
    save_on_top = True
    save_as = True


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


@admin.register(SeatClass)
class SeatClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_display_links = ('name',)


@admin.register(SeatNumber)
class SeatNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'airplane', 'seat_class', 'number')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    # readonly_fields = ('price',)
    list_display_links = ('name',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'first_name', 'last_name', 'lunch', 'luggage', 'flight',
        'datetime', 'seat_class', 'total_price', 'gate', 'seat', 'gateway_passed',
        'ticket_code', 'create_datetime'
    )
    list_editable = ['gateway_passed']
