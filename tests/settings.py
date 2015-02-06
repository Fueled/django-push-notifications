from configurations import Configuration


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
