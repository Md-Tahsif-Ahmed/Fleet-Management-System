import logging
import random
from collections import Counter

from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from django.conf import settings
from .models import Trip, Route


# logging configurations
logger = logging.getLogger('fleet_management')

# PubNub Configurations
pnconfig = PNConfiguration()
pnconfig.subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY
pnconfig.publish_key = settings.PUBNUB_PUBLISH_KEY
pnconfig.ssl = False

pubnub = PubNub(pnconfig)


def set_trip(vehicle, cycle=None):
    """
    this function automatically set a trip for provided vehicle

    :param vehicle:
    :param cycle:
    :return Trip if operation is success, None if any error occurred::
    """

    logger.debug('{} function starting'.format(set_trip.__name__))
    logger.info('checking vehicle condition')
    if vehicle.condition == 0:
        logger.info('vehicle condition is not ok')
        # vehicle condition is not ok, so
        # vehicle is not ready for trip!
        logger.info('set_trip function returning None')
        return None

    # change cycle parameter if no value passed
    logger.info('checking if cycle parameter passed')
    if cycle is None:
        logger.info('cycle parameter not passed')
        cycle = vehicle.cycle
        logger.info('assigned vehicle.cycle to cycle "{}"'.format(cycle))

    logger.debug('getting all trips')
    all_trips = Trip.objects.all().select_related('destination')

    # get routes ids of incomplete trips
    # incomplete trips are those which are assigned but not completed
    logger.debug('getting incomplete trips')
    incomplete_trips = all_trips.exclude(status=5)
    logger.debug('{} incomplete trips got'.format(incomplete_trips.count()))
    logger.debug('getting routes of incomplete trips')
    incomplete_trips_routes = [trip.destination.id for trip in incomplete_trips]

    # get all routes
    logger.debug('getting all routes')
    all_routes = Route.objects.all()
    logger.debug('{} route got'.format(all_routes.count()))

    # check if any route reserved for this vehicle
    # if so, then make trip to this route and remove reserved_for
    # fields value from this route and return.
    # otherwise exclude all routes which are reserved
    # for any vehicles!
    logger.info('checking reserved routes for this vehicle')
    reserved_routes = all_routes.filter(reserved_for=vehicle)
    if reserved_routes.exists():
        logger.info('{} reserved route found'.format(reserved_routes.count()))
        # pick first route if there multiple reserved routes
        r_route = reserved_routes.first()
        logger.info('reserved first route is {}'.format(r_route))
        r_route.reserved_for = None
        logger.info('r_route set None')
        r_route.save()
        logger.info('r_route saved')

        # make a trip!
        logger.info('making new trip')
        trip = Trip.objects.create(vehicle=vehicle, vehicle_cycle=cycle, destination=r_route)
        logger.info('new trip to {}, vehicle {}, cycle: {} assigned'.format(trip.destination, trip.vehicle, trip.vehicle_cycle))

        # update live trip-board
        try:
            logger.info('trying to publish pubnub signal')
            envelope = pubnub.publish().channel("update_board").message({
                'vehicle': trip.vehicle.model,
                'status': trip.status,
            }).sync()
            logger.info("pubnub signal publish timetoken: %d" % envelope.result.timetoken)
        except PubNubException as e:
            logger.error('pubnub error')
            logger.error(e)

        # return trip
        logger.info('new trip returning')
        logger.debug('{} function ending'.format(set_trip.__name__))
        return trip

    else:
        logger.info('no reserved route found for this vehicle')
        logger.info('filtering all routes which are not reserved for any vehicle')
        all_routes = all_routes.filter(reserved_for__isnull=True)
        logger.info('{} routes after filtering reserved routes'.format(all_routes))

    # difference between long and short route for heavy and light vehicle
    logger.info('checking vehicle type')
    if vehicle.type == 1:  # heavy
        logger.info('vehicle type is 1')
        all_routes = all_routes.filter(type=1)
        logger.info('filtering route type 1 from all_routes')
    elif vehicle.type == 2:  # light
        logger.info('vehicle type is 2')
        all_routes = all_routes.filter(type=2)
        logger.info('filtering route type 2 from all_routes')

    # get expended total routes ids
    logger.info('getting expended total routes')
    expended_total_routes = [route.id for route in all_routes for trip in range(route.max_trip)]
    logger.info('{} routes got'.format(len(expended_total_routes)))

    # remove all route id from expended_total_routes which are in incomplete_trips_routes
    # so that cleaned expended_total_routes will be inactive routes
    logger.info('getting inactive routes')
    inactive_routes = list((Counter(expended_total_routes)-Counter(incomplete_trips_routes)).elements())
    logger.info('{} inactive routes got'.format(len(inactive_routes)))

    # if there is no inactive route at this moment hold the vehicle without any new trip assigned
    if len(inactive_routes) == 0:
        logger.info('no inactive route found')
        vehicle.condition = 2
        logger.info('vehicle conditon changed to "Not Assigned"')
        vehicle.save()
        logger.info('vehicle saved')
        logger.error('returning False, without setting new trip for vehicle {}'.format(vehicle))
        return None

    # get vehicle route list from its trip history
    # trip history will retrieve by provided cycle and
    # it can be vehicle's current cycle or next cycle!
    logger.info('getting vehicle trip history for cycle {}'.format(cycle))
    vehicle_trips = all_trips.filter(vehicle=vehicle, vehicle_cycle=cycle)
    logger.info('{} trips found for cycle {}'.format(vehicle_trips.count(), cycle))
    vehicle_trips_route_list = [trip.destination.id for trip in vehicle_trips]

    # remove all route id from inactive_routes which are in vehicle_trips_route_list
    # so that cleaned expended_total_routes will be inactive routes
    logger.info('getting available routes for this vehicle')
    available_routes_for_vehicle = list((Counter(inactive_routes) - Counter(vehicle_trips_route_list)).elements())
    logger.info('{} available routes found'.format(len(available_routes_for_vehicle)))

    # set a random route for vehicle from available_routes_for_vehicle if there is any route!
    if available_routes_for_vehicle:
        logger.info('setting random route from available routes')
        random_route_id = random.choice(available_routes_for_vehicle)
        logger.info('new route id {}'.format(random_route_id))
        logger.info('getting route object for id: {}'.format(random_route_id))
        new_route = Route.objects.get(id=random_route_id)

        # make a trip!
        logger.info('making new trip')
        trip = Trip.objects.create(vehicle=vehicle, vehicle_cycle=cycle, destination=new_route)
        logger.info('new trip to {}, vehicle {}, cycle: {} assigned'.format(trip.destination, trip.vehicle, trip.vehicle_cycle))

        # update live trip-board
        try:
            logger.info('trying to publish pubnub signal')
            envelope = pubnub.publish().channel("update_board").message({
                'vehicle': trip.vehicle.model,
                'status': trip.status,
            }).sync()
            logger.info("pubnub signal publish timetoken: %d" % envelope.result.timetoken)
        except PubNubException as e:
            logger.error('pubnub error')
            logger.error(e)

        # return trip
        logger.info('new trip returning')
        logger.debug('{} function ending'.format(set_trip.__name__))
        return trip

    else:
        logger.info('no available route in this moment')
        if vehicle.cycle == cycle and len(vehicle_trips_route_list) >= len(expended_total_routes):
            logger.info('vehicles current cycle is completed')

            # current cycle of this vehicle is completed
            # upgrade vehicle cycle
            vehicle.cycle += 1
            logger.info('vehicle cycle upgraded to vehicle cycle')
            vehicle.save()
            logger.info('vehicle saved')

            # recursively call this function for retrieving new trip
            # from upgraded cycle of this vehicle
            logger.info('calling set_trip function recursively')
            return set_trip(vehicle)
        else:
            logger.info('all routes of vehicles current cycle are busy')
            # vehicles current cycle is'nt completed and
            # no route is available now for this vehicle in this cycle.
            # we're going to make a trip for next cycle, without upgrading
            # vehicles current cycle
            logger.info('calling set_trip function with extra cycle parameter incremented by 1')
            return set_trip(vehicle, cycle+1)