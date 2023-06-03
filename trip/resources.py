from import_export import resources
from import_export.fields import Field

from .models import Trip


class TripResource(resources.ModelResource):
    class Meta:
        model = Trip
        fields = ('id',
                  'date',
                  'vehicle__number',  # foreign key
                  'vehicle__type',  # foreign key
                  'vehicle_cycle',
                  'vehicle__driver__name',  # foreign key
                  'destination__name',  # foreign key
                  'leaving_time_from_dhaka',
                  'arriving_time_to_destination',
                  'leaving_time_from_destination',
                  'arriving_time_to_dhaka',
                  )
        widgets = {
            'date': {'format': '%d/%m%Y %H:%M'},
            'leaving_time_from_dhaka': {'format': '%d/%m%Y %H:%M'},
            'arriving_time_to_destination': {'format': '%d/%m%Y %H:%M'},
            'leaving_time_from_destination': {'format': '%d/%m%Y %H:%M'},
            'arriving_time_to_dhaka': {'format': '%d/%m%Y %H:%M'},
        }
