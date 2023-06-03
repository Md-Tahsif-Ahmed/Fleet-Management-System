import logging
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render

from trip.models import Trip, Driver, Route, Vehicle, VEHICLE_TYPES, ROUTE_TYPES
from trip.resources import TripResource


# logger setting
logger = logging.getLogger('fleet_management')


def reports(request):
    logger.debug('reports view starting')
    trips = Trip.objects.filter(status=5)
    logger.info('{} completed trips retrieved'.format(trips.count()))

    # checking for filtering/searching parameters
    logger.debug('request.GET parameters: "{}"'.format(request.GET))
    print(request.GET)

    # finding provided date range in GET parameters
    date_range = request.GET.get('date_range')
    if date_range:
        logger.info('date range provided: {}'.format(date_range))
        try:
            logger.info('trying to split date range')
            start_date_str = date_range.split('-')[0].strip()
            end_date_str = date_range.split('-')[1].strip()

            # get datetime object from date strings
            logger.info('getting datetime object from split dates')
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

        except Exception as e:
            logger.critical(e)
    else:
        logger.info('no date range provide')

    # if no date range provided then set default date range!
    if'start_date' not in locals():
        start_date = (datetime.today() - timedelta(days=6))
        logger.debug('default start date set to : "{}"'.format(start_date))
    if 'end_date' not in locals():
        end_date = datetime.today()
        logger.debug('default end date set to : "{}"'.format(end_date))

    # filtering based on date range
    logger.info('filtering trips based on date ranges')
    try:
        trips = trips.filter(date__gte=start_date, date__lte=end_date)
    except Exception as e:
        logger.critical(e)

    # filtering for any search value in get method
    search_query = request.GET.get('q')
    if search_query:
        logger.debug('filtering for search query "{}"'.format(search_query))
        trips = trips.filter(Q(vehicle__driver__name__icontains=search_query) |
                             Q(vehicle__number__icontains=search_query) |
                             Q(vehicle__model__icontains=search_query) |
                             Q(destination__name__icontains=search_query) |
                             Q(date__icontains=search_query)).distinct()

    # filtering based on vehicle
    vehicle_id = request.GET.get('vehicle_id')
    if vehicle_id:
        trips = trips.filter(vehicle__id=vehicle_id)

    # filtering based on vehicle type
    vehicle_type = request.GET.get('vehicle_type')
    if vehicle_type:
        trips = trips.filter(vehicle__type=vehicle_type)

    # filtering based on driver
    driver_id = request.GET.get('driver_id')
    if driver_id:
        trips = trips.filter(vehicle__driver__id=driver_id)

    # filtering based on destination
    destination = request.GET.get('destination')
    if destination:
        trips = trips.filter(destination=destination)

    # filtering based on route type
    route_type = request.GET.get('route_type')
    if route_type:
        trips = trips.filter(destination__type=route_type)

    # getting all routes for filtering
    all_routes = Route.objects.all()

    # getting all drivers for filtering
    all_drivers = Driver.objects.all()

    # getting all vehicle for filtering
    all_vehicles = Vehicle.objects.all()

    # ============== EXPORTING DATA =======================
    # if export button clicked then export data without rendering template
    is_export = request.GET.get('export')
    if is_export:
        trip_resource = TripResource()
        dataset = trip_resource.export(trips)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="trips.xls"'
        return response
    # =============== END EXPORTING ===========================

    context = {
        'trips': trips,
        'VEHICLES': all_vehicles,
        'VEHICLE_TYPES': dict(VEHICLE_TYPES),
        'DRIVERS': all_drivers,
        'DESTINATIONS': all_routes,
        'ROUTE_TYPES': dict(ROUTE_TYPES),
        'start_date':start_date.strftime('%d/%m/%Y'),
        'end_date':end_date.strftime('%d/%m/%Y'),
        'view_name': 'report',
    }
    logger.debug('reports view ending')
    return render(request, 'report/reports.html', context)


def export_report(request):
    trip_resource = TripResource()
    dataset = trip_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="trips.xls"'
    return response
