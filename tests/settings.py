from configurations import Configuration, values


class Testing(Configuration):
    SECRET_KEY = 'abc'

    INSTALLED_APPS = (
        'push_notifications',
        'tests',
        'querystring_parser',
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'testing',
        }
    }

    AUTH_USER_MODEL = 'tests.TestUser'

    DEBUG = values.BooleanValue(True)

    DJANGO_PUSH_NOTIFICATIONS = {
        'SERVICE': 'push_notifications.services.zeropush.ZeroPushService',
        'AUTH_TOKEN': '123123123'
    }
