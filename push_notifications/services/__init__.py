from django.conf import settings
from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured

# Local stuff
from .exceptions import InvalidPushNotificationError


SERVICE_NAME_KEY = 'SERVICE'

if SERVICE_NAME_KEY not in settings.DJANGO_PUSH_NOTIFICATIONS:
    raise ImproperlyConfigured("You must define '%s' for "
                               "services to work" % SERVICE_NAME_KEY)


def get_service():
    """
    Autoloading service for getting the Service that is set up
    """
    return service


def _create_service(service_name):
    try:
        # Try to get the CACHES entry for the given backend name first
        service_cls = import_string(service_name)
    except ImportError as e:
        raise InvalidPushNotificationError(
            "Could not find service '%s': %s" % (service_name, e))

    return service_cls(settings.DJANGO_PUSH_NOTIFICATIONS)

service = _create_service(settings.DJANGO_PUSH_NOTIFICATIONS['SERVICE'])
