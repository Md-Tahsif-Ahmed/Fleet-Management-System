from django import forms
from django.forms import DateTimeInput
from .models import Trip

class TripForm(forms.ModelForm):
    leaving_time_from_dhaka = forms.DateTimeField(widget=DateTimeInput(format='%Y-%m-%d %H:%M'))
    arriving_time_to_destination = forms.DateTimeField(widget=DateTimeInput(format='%Y-%m-%d %H:%M'))
    leaving_time_from_destination = forms.DateTimeField(widget=DateTimeInput(format='%Y-%m-%d %H:%M'))
    arriving_time_to_dhaka = forms.DateTimeField(widget=DateTimeInput(format='%Y-%m-%d %H:%M'))

    class Meta:
        model = Trip
        fields = ['vehicle', 'destination', 'date', 'vehicle_cycle', 'status', 'leaving_time_from_dhaka', 'arriving_time_to_destination', 'leaving_time_from_destination', 'arriving_time_to_dhaka', 'left_from_dhaka_updater', 'arrived_to_destination_updater', 'left_from_destination_updater', 'arrived_to_dhaka_updater']
