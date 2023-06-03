from django.urls import path
from .views import index, dashboard, activity, trips, add_trip, vehicles_in_dhaka, change_trip, vehicles_driver, trip_board, all_routes

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('activity/', activity, name='activity'),
    path('trips', trips, name='trips'),
     path('add_trip/', add_trip, name='add_trip'),
    path('change_trip/', change_trip, name='change_trip'),
    path('vehicles_in_dhaka/', vehicles_in_dhaka, name='vehicles_in_dhaka'),
    path('vehicles_driver/', vehicles_driver, name='vehicles_driver'),
    # path('extra_drivers/', extra_drivers, name='extra_drivers'),
    path('trip_board/', trip_board, name='trip_board'),
    path('all_routes/', all_routes, name='all_routes'),
]