from django.apps import AppConfig


class TripConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trip'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Driver'))
        registry.register(self.get_model('Vehicle'))
        registry.register(self.get_model('Route'))
        registry.register(self.get_model('Trip'))
