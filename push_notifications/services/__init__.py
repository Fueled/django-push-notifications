from threading import local
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured

# Local stuff
from .base import InvalidPushNotificationError

SERVICE_NAME_KEY = 'SERVICE'

if SERVICE_NAME_KEY not in settings.DJANGO_PUSH_NOTIFICATIONS:
    raise ImproperlyConfigured("You must define '%s' for "
                               "services to work" % SERVICE_NAME_KEY)


def get_service():
    """
    Autoloading service for getting the Service that is set up
    """
    return services[settings.DJANGO_PUSH_NOTIFICATIONS[SERVICE_NAME_KEY]]


def _create_service(service_name):
    try:
        # Try to get the CACHES entry for the given backend name first
        service_cls = import_string(service_name)
    except ImportError as e:
        raise InvalidPushNotificationError(
            "Could not find service '%s': %s" % (service_name, e))

    return service_cls(settings.DJANGO_PUSH_NOTIFICATIONS)


class ServiceHandler(object):
    """
    Handles all the automatic service loading

    Ensures that there is only one instance of the service
    """
    def __init__(self):
        self._services = local()

    def __getitem__(self, alias):
        """
        Gets fired when a item is retrieved. For example:
        zeropush = services['zeropush']
        """
        try:
            return self._services.services[alias]
        except AttributeError:
            self._services.services = {}
        except KeyError:
            pass

        cache = _create_service(alias)
        self._services.services[alias] = cache

        return cache


services = ServiceHandler()
