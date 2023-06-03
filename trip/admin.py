from django.contrib import admin

from .models import Driver, Vehicle, Route, Trip


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'nid')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'model', 'cycle', 'type', 'condition')
    list_filter = ('type', 'condition', 'cycle')


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'max_trip', 'route_order')
    list_filter = ('type', 'max_trip')


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'vehicle_cycle', 'destination', 'status')
    list_filter = ('destination', 'status', 'vehicle')