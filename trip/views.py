import logging
from collections import Counter
from datetime import datetime, timedelta
from .forms import TripForm
from django.shortcuts import render, reverse, redirect
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect

from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from actstream import action
from actstream.models import Action, user_stream

from .models import Trip, Vehicle, Driver, Route, VehicleCondition
from .models import VEHICLE_CONDITIONS, VEHICLE_TYPES, TRIP_STATUS, ROUTE_TYPES
from .utils import set_trip
from .decorators import group_required

# set logger
logger = logging.getLogger('fleet_management')

# PubNub Configurations
pnconfig = PNConfiguration()
pnconfig.subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY
pnconfig.publish_key = settings.PUBNUB_PUBLISH_KEY
pnconfig.uuid = settings.PUBNUB_UUID
pnconfig.ssl = False

pubnub = PubNub(pnconfig)

 
 
 
 

from .models import Trip, Vehicle, Driver, Route, VehicleCondition
from .models import VEHICLE_CONDITIONS, VEHICLE_TYPES, TRIP_STATUS, ROUTE_TYPES
 
 

# set logger
logger = logging.getLogger('fleet_management')

 
 


@login_required
def index(request):
    """Simple redirector to figure out where the user goes next."""
    # if request.user.designation == 1:  # OCR
    #     return HttpResponseRedirect(reverse('trips'))
    # elif request.user.designation == 2:  # Manager:
    #     return HttpResponseRedirect(reverse('change_trip'))
    return HttpResponseRedirect(reverse('dashboard'))

@login_required
def dashboard(request):
    logger.debug('{} view starting'.format(dashboard.__name__))

    all_trips = Trip.objects.all()

    # last trips left from dhaka
    last_trips_left_from_dhaka = all_trips.filter(status__gte=2).order_by('-leaving_time_from_dhaka')[:10]

    # last scheduled trips
    last_scheduled_trips = all_trips.order_by('-id')[:10]

    # average trip times
    routes = Route.objects.all()[:10]
    route_list = [route.name for route in routes]

    trip_times = {}
    for route in route_list:
        trip_timestamps = []
        route_trips = all_trips.filter(destination__name__icontains=route)
        for trip in route_trips:
            t_time = trip.arriving_time_to_dhaka.timestamp() - trip.leaving_time_from_dhaka.timestamp()
            trip_timestamps.append(t_time)

        try:
            average_timestamp = sum(trip_timestamps) / float(len(trip_timestamps))
        except ZeroDivisionError:
            average_timestamp = 0

        trip_times[route] = datetime.utcfromtimestamp(average_timestamp).hour

    # vehicles in maintenance last 10 days
    vehicle_conditions = VehicleCondition.objects.filter(condition=False).select_related('vehicle')
    vehicles_in_maintenance = {}
    for i in range(11): # for 10 days
        d = datetime.today() - timedelta(days=i)
        vehicles_in_maintenance[d.strftime('%d/%m/%Y')] = vehicle_conditions.filter(date__date=d).count()

    context = {
        'last_trips_left_from_dhaka':last_trips_left_from_dhaka,
        'last_scheduled_trips':last_scheduled_trips,
        'route_list': route_list,
        'trip_times': trip_times,
        'vehicles_in_maintenance': vehicles_in_maintenance,
        'view_name': 'dashboard',  # used for sidebar menu active class
    }
    logger.debug('{} view ending'.format(dashboard.__name__))
    return render(request, 'trip/dashboard.html', context)


@login_required
@group_required('Manager')
def activity(request):
    # activity_stream = user_stream(request.user, with_user_activity=True)[:100]
    activity_stream = Action.objects.all()

    context = {
        'activity_stream': activity_stream,
    }
    return render(request, 'trip/activity.html', context)



@login_required
def vehicles_in_dhaka(request):
    logger.debug('{} view starting'.format(vehicles_in_dhaka.__name__))
    vehicles = Vehicle.objects.filter(Q(condition=0) |
                                      Q(condition=2)).distinct()

    # filtering for any search value in get method
    search_query = request.GET.get('q')
    if search_query:
        logger.debug('filtering for search query "{}"'.format(search_query))
        vehicles = vehicles.filter(Q(driver__name__icontains=search_query) |
                                   Q(number__icontains=search_query) |
                                   Q(model__icontains=search_query)).distinct()

    # filtering for type value in get method
    type_filter_query = request.GET.get('type')
    if type_filter_query:
        logger.debug('filtering for type filter "{}"'.format(type_filter_query))
        vehicles = vehicles.filter(type=type_filter_query)

    # filtering for condition value in get method
    condition_filter_query = request.GET.get('condition')
    if condition_filter_query:
        logger.debug('filtering for condition filter "{}"'.format(condition_filter_query))
        vehicles = vehicles.filter(condition=condition_filter_query)

    logger.debug('starting pagination settings')
    page = request.GET.get('page', 1)

    paginator = Paginator(vehicles, 10)
    try:
        vehicles = paginator.page(page)
        logger.debug('velid page number "{}" get'.format(page))
    except PageNotAnInteger:
        vehicles = paginator.page(1)
        logger.debug('page not an integer')
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)
        logger.debug('empty page')
    logger.debug('pagination settings end')

    if request.method == 'POST':
        logger.info('request method is POST')
        logger.info(request.POST)
        vehicle_id = request.POST.get('ok')
        if vehicle_id:
            logger.info('vehicle id "{}"'.format(vehicle_id))
            try:
                logger.info('trying to retrieve vehicle')
                vehicle = Vehicle.objects.get(id=vehicle_id)
                logger.info('found vehicle id {}'.format(vehicle_id))
                vehicle.condition = 1
                logger.info('vehicle condition changed to "{}"'.format(vehicle.condition))
                vehicle.save()
                logger.info('vehicle saved')
                messages.success(request, 'Vehicle Condition Updated')
                action.send(request.user, verb='Changed Vehicle {} Conditoin To: {}'.format(vehicle, vehicle.condition))

                logger.info('calling set_trip function')
                new_trip = set_trip(vehicle)
                logger.info('set_trip function returned')
                if new_trip:
                    logger.info('New Trip To: {} Assigned To This Vehicle'.format(new_trip.destination))
                    messages.info(request, 'Vehicle {} is OK, New Trip To: {} Assigned To This Vehicle'.format(vehicle, new_trip.destination))
                else:
                    logger.warning('Vehicle is OK, No New Trip Assigned')
                    messages.error(request, "Vehicle {} is OK, NO Trip Added Automatically!".format(vehicle))

            except Vehicle.DoesNotExist:
                logger.warning('vehicle id {} not exists'.format(vehicle_id))
                messages.error(request, 'Vehicle not Exists')

            except Exception as e:
                logger.critical(e)

        logger.info('post method code block ending'
                    )
    context = {
        'vehicles': vehicles,
        'VEHICLE_TYPES': dict(VEHICLE_TYPES),  # vehicle types for filtering
        'VEHICLE_CONDITIONS': dict(VEHICLE_CONDITIONS),  # vehicle conditions for filtering
        'view_name': 'vehicles_in_dhaka',  # used for sidebar menu active class
    }
    logger.debug('{} view ending'.format(vehicles_in_dhaka.__name__))
    return render(request, "trip/vehicles_in_dhaka.html", context)



@login_required
@group_required('OCR')
def trips(request):
    logger.debug('{} view starting'.format(trips.__name__))
    all_trips = Trip.objects.exclude(status=5)
    logger.debug('retrieve "{}" trips'.format(all_trips.count()))

    # filtering for any search value in get method
    search_query = request.GET.get('q')
    if search_query:
        logger.debug('filtering for search query "{}"'.format(search_query))
        all_trips = all_trips.filter(Q(vehicle__driver__name__icontains=search_query) |
                                   Q(vehicle__number__icontains=search_query) |
                                   Q(vehicle__model__icontains=search_query) |
                                   Q(destination__name__icontains=search_query)).distinct()

    # filtering for vehicle type value in get method
    vehicle_type_filter_query = request.GET.get('vehicle_type')
    if vehicle_type_filter_query:
        logger.debug('filtering for vehicle type filter query "{}"'.format(vehicle_type_filter_query))
        all_trips = all_trips.filter(vehicle__type=vehicle_type_filter_query)

    # filtering for route type value in get method
    route_type_filter_query = request.GET.get('route_type')
    if route_type_filter_query:
        logger.debug('filtering for route type filter query "{}"'.format(route_type_filter_query))
        all_trips = all_trips.filter(destination__type=route_type_filter_query)

    # filtering for destination value in get method
    destination_filter_query = request.GET.get('destination')
    if destination_filter_query:
        logger.debug('filtering for destination filter query "{}"'.format(destination_filter_query))
        all_trips = all_trips.filter(destination__id=destination_filter_query)

    # filtering for trip status value in get method
    status_filter_query = request.GET.get('status')
    if status_filter_query:
        logger.debug('filtering for trip status filter query "{}"'.format(status_filter_query))
        all_trips = all_trips.filter(status=status_filter_query)

    logger.debug('starting pagination settings')
    page = request.GET.get('page', 1)

    paginator = Paginator(all_trips, 10)
    try:
        all_trips = paginator.page(page)
    except PageNotAnInteger:
        all_trips = paginator.page(1)
    except EmptyPage:
        all_trips = paginator.page(paginator.num_pages)
    logger.debug('pagination settings end')

    if request.method == 'POST':
        logger.info('request method is POST')
        logger.info(request.POST)
        trip_id = request.POST.get('save')
        if trip_id:
            logger.info('got trip id {}'.format(trip_id))
            try:
                logger.info('trying to find trip')
                trip = Trip.objects.get(id=trip_id)
                logger.info('found trip id {}'.format(trip_id))

                if request.POST.get('is_left_from_dhaka'):
                    logger.info('vehicle is left from dhaka')
                    trip.leaving_time_from_dhaka = datetime.strptime(request.POST.get('leaving_time_from_dhaka'),'%d/%m/%Y %H:%M %p') if request.POST.get('leaving_time_from_dhaka') else now()
                    logger.info('assigned leaving time {}'.format(trip.leaving_time_from_dhaka))
                    trip.status = 2
                    logger.info('assigned status to {}'.format(trip.status))
                    trip.left_from_dhaka_updater = request.user
                    logger.info('assigned {} to leaving time updater'.format(request.user))
                    trip.save()
                    logger.info('trip saved')
                    messages.info(request, 'Vehicle "{}" Left From Dhaka'.format(trip.vehicle))
                    # messages.success(request, 'Information Saved Successfully')
                    action.send(request.user, verb='Set Vehicle {} ')

                    # update live trip-board panel
                    try:
                        logger.info('trying to publish pubnub message')
                        envelope = pubnub.publish().channel("update_board").message({
                            'vehicle': trip.vehicle.model,
                            'status': trip.status,
                        }).sync()
                        logger.info("pubnub publish timetoken: %d" % envelope.result.timetoken)
                    except PubNubException as e:
                        logger.error(e)

                elif request.POST.get('is_arrived_to_destination'):
                    logger.info('vehicle is arrived to destination')
                    trip.arriving_time_to_destination = datetime.strptime(request.POST.get('arriving_time_to_destination'),'%d/%m/%Y %H:%M %p') if request.POST.get('arriving_time_to_destination') else now()
                    logger.info('assigned arriving time {}'.format(trip.arriving_time_to_destination))
                    trip.status = 3
                    logger.info('assigned status to {}'.format(trip.status))
                    trip.arrived_to_destination_updater = request.user
                    logger.info('assigned {} to arriving time updater'.format(request.user))
                    trip.save()
                    logger.info('trip saved')
                    messages.info(request, 'Vehicle "{}" Arrived To Destination'.format(trip.vehicle))
                    # messages.success(request, 'Information Saved Successfully')

                elif request.POST.get('is_left_from_destination'):
                    logger.info('vehicle is left from destination')
                    trip.leaving_time_from_destination = datetime.strptime(request.POST.get('leaving_time_from_destination'),'%d/%m/%Y %H:%M %p') if request.POST.get('leaving_time_from_destination') else now()
                    logger.info('assigned leaving time {}'.format(trip.leaving_time_from_destination))
                    trip.status = 4
                    logger.info('assigned status to {}'.format(trip.status))
                    trip.left_from_destination_updater = request.user
                    logger.info('assigned {} to leaving time updater'.format(request.user))
                    trip.save()
                    logger.info('trip saved')
                    messages.info(request, 'Vehicle "{}" Left From Destination'.format(trip.vehicle))
                    # messages.success(request, 'Information Saved Successfully')

                elif request.POST.get('is_arrived_to_dhaka'):
                    logger.info('vehicle is arrived to dhaka')
                    trip.arriving_time_to_dhaka = datetime.strptime(request.POST.get('arriving_time_to_dhaka'),'%d/%m/%Y %H:%M %p') if request.POST.get('arriving_time_to_dhaka') else now()
                    logger.info('assigned arriving time {}'.format(trip.arriving_time_to_destination))
                    trip.status = 5
                    logger.info('assigned status to {}'.format(trip.status))
                    trip.arrived_to_dhaka_updater = request.user
                    logger.info('assigned {} to arriving time updater'.format(request.user))

                    trip.save()
                    logger.info('trip saved')
                    messages.info(request, 'Vehicle "{}" Arrived To Dhaka From "{}" '.format(trip.vehicle, trip.destination))
                    # messages.success(request, 'Information Saved Successfully')

                    # checking vehicle condition for new trip
                    logging.info('vehicle condition checking')
                    condition = request.POST.get('is_arrived_to_dhaka')
                    if condition == 'ok':
                        logger.info('vehicle condition is ok')
                        # set new trip
                        logger.info('getting vehicle object')
                        vehicle = Vehicle.objects.get(id=trip.vehicle.id)
                        logger.info('got vehicle id {}'.format(vehicle.id))
                        logger.info('calling set_trip function')
                        new_trip = set_trip(vehicle)
                        logger.info('set_trip function returned')
                        if new_trip:
                            logger.info('new trip to {} assigned to vehicle {}'.format(new_trip.destination, vehicle))
                            messages.info(request, 'Vehicle {} is OK, New Trip to "{}" Assigned To This Vehicle'.format(vehicle, new_trip.destination))
                        else:
                            logger.warning('Vehicle is OK, No New Trip Assigned')
                            messages.error(request, "Vehicle {} is OK, NO New Trip Added Automatically!".format(vehicle))
                    else:
                        logger.info('vehicle condition is not ok')
                        logger.info('getting vehicle object')
                        vehicle = Vehicle.objects.get(id=trip.vehicle.id)
                        vehicle.condition = 0
                        logger.info('vehicle condition changed to {}'.format(vehicle.condition))
                        vehicle.save()
                        logger.info('vehicle saved')

                        # create a VehicleCondition object for this vehicle
                        logger.debug('creating new VehicleCondition object')
                        VehicleCondition.objects.create(vehicle= vehicle)
                        logger.debug('new VehicleConditon created for vehicle {}'.format(vehicle))

                        messages.warning(request, 'Vehicle {} is Not OK, New Trip Not Added'.format(trip.vehicle.id))
                else:
                    logger.warning('No information changed on trip {}'.format(trip.id))
                    messages.warning(request, 'NO Information Changed On Trip: "{}"'.format(trip_id))

            except Trip.DoesNotExist:
                logger.error('trip not exists')
                messages.error(request, 'Trip not Exists')
            except Exception as e:
                logger.critical(e)

    # all routes for filtering destination
    all_routes = Route.objects.all()

    logger.debug('making context dict')
    context = {
        'trips': all_trips,
        'VEHICLE_TYPES': dict(VEHICLE_TYPES),  # vehicle types for filtering
        'ROUTE_TYPES': dict(ROUTE_TYPES),  # route types for filtering
        'TRIP_STATUS': dict(TRIP_STATUS),  # trip status for filtering
        'DESTINATIONS': all_routes,  # destination for filtering
        'CURRENT_DATE_TIME': datetime.now().strftime('%d/%m/%Y %H:%M %p'),  # current time
        'view_name': 'trips',  # used for sidebar menu active class
    }
    logger.debug('{} view ending'.format(trips.__name__))
    return render(request, "trip/trips.html", context)

def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save()
            return redirect('trips')
    else:
        form = TripForm()
    return render(request, 'trip/add_trip.html', {'form': form})


@login_required
@group_required('Manager')
def change_trip(request):
    logger.debug('{} view starting'.format(change_trip.__name__))
    all_trips = Trip.objects.exclude(status=5)
    logger.debug('retrieve "{}" trips'.format(all_trips.count()))

    # filtering for any search value in get method
    search_query = request.GET.get('q')
    if search_query:
        logger.debug('filtering for search query "{}"'.format(search_query))
        all_trips = all_trips.filter(Q(vehicle__driver__name__icontains=search_query) |
                                   Q(vehicle__number__icontains=search_query) |
                                   Q(vehicle__model__icontains=search_query) |
                                   Q(destination__name__icontains=search_query)).distinct()

    # filtering for vehicle type value in get method
    vehicle_type_filter_query = request.GET.get('vehicle_type')
    if vehicle_type_filter_query:
        logger.debug('filtering for vehicle type filter query "{}"'.format(vehicle_type_filter_query))
        all_trips = all_trips.filter(vehicle__type=vehicle_type_filter_query)

    # filtering for route type value in get method
    route_type_filter_query = request.GET.get('route_type')
    if route_type_filter_query:
        logger.debug('filtering for route type filter query "{}"'.format(route_type_filter_query))
        all_trips = all_trips.filter(destination__type=route_type_filter_query)

    # filtering for destination value in get method
    destination_filter_query = request.GET.get('destination')
    if destination_filter_query:
        logger.debug('filtering for destination filter query "{}"'.format(destination_filter_query))
        all_trips = all_trips.filter(destination__id=destination_filter_query)

    # filtering for trip status value in get method
    status_filter_query = request.GET.get('status')
    if status_filter_query:
        logger.debug('filtering for trip status filter query "{}"'.format(status_filter_query))
        all_trips = all_trips.filter(status=status_filter_query)

    if request.method == 'POST':
        logger.info('request method is POST')
        logger.info(request.POST)
        trip_id = request.POST.get('save')
        if trip_id:
            logger.info('got trip id {}'.format(trip_id))
            try:
                logger.info('trying to find trip')
                trip = Trip.objects.get(id=trip_id)
                logger.info('found trip id {}'.format(trip_id))

                logger.info('checking if this vehicle is on the way')
                if trip.status == 1:
                    logger.info('vehicle not left dhaka')
                    vehicle_id = request.POST.get('change_vehicle')
                    if vehicle_id:
                        logger.info('vehicle id {} provided'.format(vehicle_id))
                        try:
                            # find new vahicle, assign to trip, change its condition
                            # find old vehicle of this trip, change condition, save!
                            logger.info('trying to find vehicle')
                            vehicle = Vehicle.objects.get(id=vehicle_id)
                            logger.info('geting existing vehicle')
                            existing_vehicle = Vehicle.objects.get(id=trip.vehicle.id)
                            logger.info('assign vehicle {} to trip'.format(vehicle))
                            trip.vehicle = vehicle
                            trip.save()
                            logger.info('trip vehicle changed')
                            logger.info('existing vehicle condition changing to 2')
                            existing_vehicle.condition = 2
                            existing_vehicle.save()
                            logger.info('existing vehicle saved')
                            logger.info('new vehicle condition changing to 1')
                            vehicle.condition = 1
                            vehicle.save()
                            logger.info('new vehicle saved')
                            messages.info(request, 'Vehicle "{}" Assigned To Destination "{}"'.format(vehicle, trip.destination))

                            # update live trip-board panel
                            try:
                                logger.info('trying to publish pubnub message')
                                envelope = pubnub.publish().channel("update_board").message({
                                    'vehicle': trip.vehicle.model,
                                    'status': trip.status,
                                }).sync()
                                logger.info("pubnub publish timetoken: %d" % envelope.result.timetoken)
                            except PubNubException as e:
                                logger.error(e)
                        except Vehicle.DoesNotExist:
                            logger.error('vehicle id {} not exists')
                            messages.error(request, 'Vehicle ID: {} Not Exists')
                        except Exception as e:
                            logger.critical(e)

                    route_id = request.POST.get('change_destination')
                    if route_id:
                        logger.info('route id {} provided'.format(route_id))
                        try:
                            logger.info('trying to find route')
                            route = Route.objects.get(id=route_id)
                            trip.destination = route
                            trip.save()
                            logger.info('trip destination changed')
                            messages.info(request, 'Destination {} Assigned To Trip {}'.format(route, trip.id))

                            # update live trip-board panel
                            try:
                                logger.info('trying to publish pubnub message')
                                envelope = pubnub.publish().channel("update_board").message({
                                    'vehicle': trip.vehicle.model,
                                    'status': trip.status,
                                }).sync()
                                logger.info("pubnub publish timetoken: %d" % envelope.result.timetoken)
                            except PubNubException as e:
                                logger.error(e)
                        except Driver.DoesNotExist:
                            logger.error('route id {} not exists')
                            messages.error(request, 'Destination ID: {} Not Exists')
                        except Exception as e:
                            logger.critical(e)
                else:
                    logger.info('this trip is on the way')
                    messages.error(request, 'Vehicle Of This Trip Is Left From Dhaka')

            except Trip.DoesNotExist:
                logger.error('trip id {} not exists')
                messages.error(request, 'Trip ID: {} Not Exists')
            except Exception as e:
                logger.critical(e)

    # all routes for filtering destination
    all_routes = Route.objects.all()

    # retrieve drivers without vehicles for changing any vehicles driver
    logger.debug("getting all vehicles which are ok but not assigned to any trip")
    not_assigned_vehicles = Vehicle.objects.filter(condition=2)

    # retrieve inactive routes
    logger.debug('getting all inactive routes')
    # get routes ids of incomplete trips
    # incomplete trips are those which are assigned but not completed
    logger.debug('getting incomplete trips')
    incomplete_trips = all_trips.exclude(status=5)
    logger.debug('{} incomplete trips got'.format(incomplete_trips.count()))
    logger.debug('getting routes of incomplete trips')
    incomplete_trips_routes = [trip.destination.id for trip in incomplete_trips]

    logger.info('getting expended total routes')
    expended_total_routes = [route.id for route in all_routes for trip in range(route.max_trip)]
    logger.info('{} routes got'.format(len(expended_total_routes)))

    # remove all route id from expended_total_routes which are in incomplete_trips_routes
    # so that cleaned expended_total_routes will be inactive routes
    logger.info('getting inactive routes ids')
    inactive_routes_list = list((Counter(expended_total_routes) - Counter(incomplete_trips_routes)).elements())
    logger.info('{} inactive routes got'.format(len(inactive_routes_list)))
    logger.info('getting routes queryset of inactive_routes_list')
    inactive_routes = all_routes.filter(id__in=inactive_routes_list)

    # ======== START PAGINATOR =====================
    logger.debug('starting pagination settings')
    page = request.GET.get('page', 1)

    paginator = Paginator(all_trips, 10)
    try:
        all_trips = paginator.page(page)
    except PageNotAnInteger:
        all_trips = paginator.page(1)
    except EmptyPage:
        all_trips = paginator.page(paginator.num_pages)
    logger.debug('pagination settings end')
    # ================ END PAGINATOR ================

    logger.debug('making context dict')
    context = {
        'trips': all_trips,
        'not_assigned_vehicles': not_assigned_vehicles,
        'inactive_routes': inactive_routes,
        'VEHICLE_TYPES': dict(VEHICLE_TYPES),  # vehicle types for filtering
        'ROUTE_TYPES': dict(ROUTE_TYPES),  # route types for filtering
        'TRIP_STATUS': dict(TRIP_STATUS),  # trip status for filtering
        'DESTINATIONS': all_routes,  # destination for filtering
        'view_name': 'change_trip',  # used for sidebar menu active class
    }
    logger.debug('{} view ending'.format(change_trip.__name__))
    return render(request, "trip/change_trip.html", context)


@login_required
@group_required('Manager')
def vehicles_driver(request):
    logger.debug('{} view starting'.format(vehicles_driver.__name__))
    vehicles = Vehicle.objects.all()

    # filtering for any search value in get method
    search_query = request.GET.get('q')
    if search_query:
        logger.debug('filtering for search query "{}"'.format(search_query))
        vehicles = vehicles.filter(Q(driver__name__icontains=search_query) |
                                   Q(number__icontains=search_query) |
                                   Q(model__icontains=search_query)).distinct()

    # filtering for type value in get method
    type_filter_query = request.GET.get('type')
    if type_filter_query:
        logger.debug('filtering for type filter query "{}"'.format(type_filter_query))
        vehicles = vehicles.filter(type=type_filter_query)

    # filtering for condition value in get method
    condition_filter_query = request.GET.get('condition')
    if condition_filter_query:
        logger.debug('filtering for condition filter query "{}"'.format(condition_filter_query))
        vehicles = vehicles.filter(condition=condition_filter_query)

    # retrieve drivers without vehicles for changing any vehicles driver
    logger.debug("getting all 'drivers without vehicle'")
    extra_drivers = Driver.objects.filter(vehicle=None)

    # pagination settings start
    page = request.GET.get('page', 1)

    logger.debug('starting pagination settings')
    paginator = Paginator(vehicles, 10)
    try:
        vehicles = paginator.page(page)
    except PageNotAnInteger:
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)
    logger.debug('pagination settings end')

    context = {
        'vehicles': vehicles,
        'extra_drivers': extra_drivers,
        'VEHICLE_TYPES': dict(VEHICLE_TYPES),  # vehicle types for filtering
        'VEHICLE_CONDITIONS': dict(VEHICLE_CONDITIONS),  # vehicle conditions for filtering
        'view_name': 'vehicles_driver',  # used for sidebar menu active class
    }

    if request.method == 'POST':
        logger.info('request method is POST')
        logger.info(request.POST)
        vehicle_id = request.POST.get('save')
        if vehicle_id:
            logger.info('got vehicle id {}'.format(vehicle_id))
            driver_id = request.POST.get('driver')
            logger.info('got driver id {}'.format(driver_id))
            try:
                logger.info('trying to get vehicle object of id "{}"'.format(vehicle_id))
                vehicle = Vehicle.objects.get(id=vehicle_id)

                logger.info('checking if the vehicle is on the way')
                running_trip_of_this_vehicle = Trip.objects.exclude(status=5).exclude(status=1).filter(vehicle=vehicle).exists()
                if running_trip_of_this_vehicle:
                    logger.info('vehicle {} on the way'.format(vehicle))
                    messages.error(request, "This Vehicle Is On The Way!")
                    logger.info('returning this view without any action')
                    return render(request, 'trip/vehicles_driver.html', context)

                # if the vehicle in dhaka then its driver will change
                logger.info('vehicle {} in dhaka'.format(vehicle))
                logger.info('getting driver object of id {}'.format(driver_id))
                driver = Driver.objects.get(id=driver_id)
                logger.info('assigning driver: {} to vehicle: {}'.format(driver, vehicle))
                vehicle.driver = driver
                logger.info('assigning {} to vehicle updater'.format(request.user))
                vehicle.updater = request.user
                vehicle.save()
                logger.info('vehicle saved')
                messages.info(request, 'Driver: "{}" Assigned to Vehicle: "{}"'.format(driver, vehicle))

                # update live trip-board panel
                try:
                    logger.info('trying to publish pubnub message')
                    envelope = pubnub.publish().channel("update_board").message({
                        'vehicle': vehicle.model,
                        'status': vehicle.condition,
                    }).sync()
                    logger.info("pubnub publish timetoken: %d" % envelope.result.timetoken)
                except PubNubException as e:
                    logger.error(e)

            except Vehicle.DoesNotExist:
                logger.error('vehicle {} not exists'.format(vehicle_id))
                messages.error(request, "Vehicle Not Exist")
            except Driver.DoesNotExist:
                logger.error('driver {} not exists'.format(driver_id))
                messages.error(request, 'Driver Not Exist')
            except Exception as e:
                logger.critical(e)

    logger.debug('{} view ending'.format(vehicles_driver.__name__))
    return render(request, 'trip/vehicles_driver.html', context)


@login_required
@group_required('Manager')
def all_routes(request):
    logger.debug('{} view starting'.format(all_routes.__name__))

    if request.method == 'POST':
        logger.info('request method is POST')
        logger.info(request.POST)

        # changing the route condition if clicked on save button
        route_id = request.POST.get('save')
        if route_id:
            try:
                logger.info('trying to find route id : {}'.format(route_id))
                route = Route.objects.get(id = route_id)
                logger.info('route "{}" found'.format(route))
                logger.info('route is_disabled value changing')
                route.is_disabled = not route.is_disabled
                logger.info('route is_disabled value now is: {}'.format(route.is_disabled))
                route.save()
                logger.info('route saved')
                messages.info(request, 'Route {} Is Now {}'.format(route, 'Disabled' if route.is_disabled else 'Enabled'))
            except Route.DoesNotExist:
                logger.error('route id {} not found'.format(route_id))
                messages.error(request, 'Route Id {} Not Found'.format(route_id))
            except Exception as e:
                logging.critical(e)

        # setting the reserved vehicle if clicked on reserve button
        route_reserved = request.POST.get('reserve')
        if route_reserved:
            try:
                logger.info('trying to find route id : {}'.format(route_reserved))
                route = Route.objects.get(id = route_reserved)
                logger.info('route "{}" found'.format(route))
                logger.info('finding vehicle for reserve')
                reserved_for = request.POST.get('vehicle')
                if reserved_for:
                    try:
                        logger.info('trying to find vehicle id : {}'.format(reserved_for))
                        vehicle = Vehicle.objects.get(id=reserved_for)
                        logger.info('vehicle {} found'.format(vehicle))

                        logger.info('changing routes reserved_for value')
                        route.reserved_for = vehicle
                        route.save()
                        logger.info('route saved')
                        messages.info(request, 'Route {} Is Now Reserved For: {}'.format(route.name, vehicle.number))
                    except Vehicle.DoesNotExist:
                        logger.error('vehicle id {} not found'.format(reserved_for))
                        messages.error(request, 'Vehicle Id {} Not Found'.format(reserved_for))
                    except Exception as e:
                        logging.critical(e)

            except Route.DoesNotExist:
                logger.error('route id {} not found'.format(route_id))
                messages.error(request, 'Route Id {} Not Found'.format(route_id))
            except Exception as e:
                logging.critical(e)

        # removing the reserved vehicle if clicked on remove button
        route_remove_reserved = request.POST.get('remove')
        if route_remove_reserved:
            try:
                logger.info('trying to find route id : {}'.format(route_remove_reserved))
                route = Route.objects.get(id=route_remove_reserved)
                logger.info('route "{}" found'.format(route))

                logger.info('removing reserved_for value')
                route.reserved_for = None
                route.save()
                logger.info('route saved')
                messages.info(request,
                              'Route {} Is Not Reserved For Any Vehicle.'.format(route.name))
            except Route.DoesNotExist:
                logger.error('route id {} not found'.format(route_id))
                messages.error(request, 'Route Id {} Not Found'.format(route_id))
            except Exception as e:
                logging.critical(e)

        # setting the max_trip if clicked on change_max_trip button
        route_id = request.POST.get('change_max_trip')
        if route_id:
            try:
                logger.info('trying to find route id : {}'.format(route_id))
                route = Route.objects.get(id=route_id)
                logger.info('route "{}" found'.format(route))

                logger.info('changing max_trip value')
                route.max_trip = request.POST.get('max_trip_value', route.max_trip)
                route.save()
                logger.info('route saved')
                messages.info(request,
                              'Max Trip Of Route {} Is Now "{}"'.format(route.name, route.max_trip))

            except Route.DoesNotExist:
                logger.error('route id {} not found'.format(route_id))
                messages.error(request, 'Route Id {} Not Found'.format(route_id))
            except Exception as e:
                logging.critical(e)

    logger.debug('getting all routes including disabled routes')
    routes_with_disabled = Route.objects.all_with_disabled()

    # filtering for any search value in get method
    search_query = request.GET.get('q')
    if search_query:
        logger.debug('filtering for search query "{}"'.format(search_query))
        routes_with_disabled = routes_with_disabled.filter(Q(name__icontains=search_query)).distinct()

    # filtering for type value in get method
    type_filter_query = request.GET.get('type')
    if type_filter_query:
        logger.debug('filtering for type filter query "{}"'.format(type_filter_query))
        routes_with_disabled = routes_with_disabled.filter(type=type_filter_query)

    # filtering for condition value in get method
    condition_filter_query = request.GET.get('condition')
    if condition_filter_query:
        logger.debug('filtering for condition filter query "{}"'.format(condition_filter_query))
        # this line below must be changed to choices field in model
        condition_filter_query = not bool(int(condition_filter_query))
        routes_with_disabled = routes_with_disabled.filter(is_disabled=condition_filter_query)

    # pagination settings start
    page = request.GET.get('page', 1)

    logger.debug('starting pagination settings')
    paginator = Paginator(routes_with_disabled, 10)
    try:
        routes_with_disabled = paginator.page(page)
    except PageNotAnInteger:
        routes_with_disabled = paginator.page(1)
    except EmptyPage:
        routes_with_disabled = paginator.page(paginator.num_pages)
    logger.debug('pagination settings end')

    # vehicle list for reserving
    vehicles = Vehicle.objects.all()

    # max length of max trip
    max_length_of_max_trip = range(1, 11)

    context = {
        'routes':routes_with_disabled,
        'max_length_of_max_trip':max_length_of_max_trip,
        'vehicles': vehicles,
        'ROUTE_TYPES': dict(ROUTE_TYPES),  # route types for filtering
        'view_name': 'all_routes',  # used for sidebar menu active class
    }
    logger.debug('{} view ending'.format(trip_board.__name__))
    return render(request, 'trip/all_routes.html', context)


@login_required
def trip_board(request):
    logger.debug('{} view starting'.format(trip_board.__name__))
    # trips assigned, but not left from dhaka.
    all_trips = Trip.objects.filter(status=1).order_by('-date')
    # long trip destination is 1
    long_trips = all_trips.filter(destination__type=1)
    # short trip destination i 2
    short_trips = all_trips.filter(destination__type=2)

    context = {
        'long_trips': long_trips,
        'short_trips': short_trips,
        'subscribe_key': settings.PUBNUB_SUBSCRIBE_KEY,  # for pubnub listening
        'view_name': 'trip_board',  # used for sidebar menu active class
    }
    logger.debug('{} view ending'.format(trip_board.__name__))
    return render(request, 'trip/trip_board.html', context)
 