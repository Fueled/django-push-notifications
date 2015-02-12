from configurations import Configuration, values


class Testing(Configuration):
    SECRET_KEY = 'abc'

    INSTALLED_APPS = (
        'push_notifications',
        'tests',
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'testing',
        }
    }

    AUTH_USER_MODEL = 'tests.TestUser'

    DEBUG = values.BooleanValue(True)
