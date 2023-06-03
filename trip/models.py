import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.timezone import now


# choices field for universal use
VEHICLE_TYPES = (
        (1, 'Heavy'),
        (2, 'Light'),
        (3, 'Mid Loaded'),
    )

VEHICLE_CONDITIONS = (
        (0, 'Not OK'),
        (1, 'OK'),
        (2, 'Not Assigned'),
    )

ROUTE_TYPES = (
        (1, 'Long'),
        (2, 'Short'),
        (3, 'Medium'),
    )

TRIP_STATUS = (
        (1, 'Trip Assigned'),
        (2, 'Left From Dhaka'),
        (3, 'Arrived To Destination'),
        (4, 'Left From Destination'),
        (5, 'Completed'),
    )


class Driver(models.Model):
    name = models.CharField(max_length=255)
    phone = models.IntegerField(null=True, blank=True)
    nid = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'drivers'


class Vehicle(models.Model):

    def pick_a_difault_driver(self):
        """this function will return a 'driver without vehicle' """
        driver = Driver.objects.filter(vehicle=None).first()
        return driver.id

    number = models.CharField(max_length=127)
    model = models.CharField(max_length=127, null=True, blank=True)
    type = models.IntegerField(default=1, choices=VEHICLE_TYPES)
    using_date = models.DateField(default=now)

    @property
    def get_type(self):
        """
        this method will return full type of vehicle
        :return STR:
        """
        return dict(VEHICLE_TYPES).get(self.type)

    cycle = models.IntegerField(default=1)
    condition = models.IntegerField(default=0, choices=VEHICLE_CONDITIONS)

    @property
    def get_condition(self):
        """
        this method will return full condition of vehicle
        :return STR:
        """
        return dict(VEHICLE_CONDITIONS).get(self.condition)

    driver = models.OneToOneField(Driver, on_delete=models.SET(pick_a_difault_driver))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updater = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='updated_vehicles')

    def __str__(self):
        return self.number

    class Meta:
        db_table = 'vehicles'


class RouteManager(models.Manager):
    def all(self):
        return self.filter(is_disabled=False)

    def all_with_disabled(self):
        return self.filter()


class Route(models.Model):
    name = models.CharField(max_length=127)
    type = models.IntegerField(default=1, choices=ROUTE_TYPES)

    @property
    def get_type(self):
        """
        this method will return full type of route
        :return STR:
        """
        return dict(ROUTE_TYPES).get(self.type)

    max_trip = models.IntegerField(default=1)
    route_order = models.IntegerField(null=True, blank=True)

    reserved_for = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)

    is_disabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RouteManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'routes'


class VehicleCondition(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='conditions')
    date = models.DateTimeField(default=now)
    condition = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehicle.number

    class Meta:
        db_table = 'vehicle_conditions'


class Trip(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    destination = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    vehicle_cycle = models.IntegerField()
    status = models.IntegerField(default=1, choices=TRIP_STATUS)

    @property
    def get_status(self):
        """
        this method will return full status string
        :return STR:
        """
        return dict(TRIP_STATUS).get(self.status)

    leaving_time_from_dhaka = models.DateTimeField(default=now)
    left_from_dhaka_updater = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='trips_updated_from_dhaka')

    arriving_time_to_destination = models.DateTimeField(default=now)
    arrived_to_destination_updater = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='trips_updated_to_destination')

    leaving_time_from_destination = models.DateTimeField(default=now)
    left_from_destination_updater = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='trips_updated_from_destination')

    arriving_time_to_dhaka = models.DateTimeField(default=now)
    arrived_to_dhaka_updater = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='trips_updated_to_dhaka')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "trip: {}, vehicle: {}, destination: {}".format(self.id, self.vehicle.number, self.destination.name)

    class Meta:
        db_table = 'trips'
        ordering = ['-id', '-date', 'status']