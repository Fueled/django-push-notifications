from configurations import Configuration


class Testing(Configuration):
    SECRET_KEY = 'abc'

    INSTALLED_APPS = (
        "push_notifications",
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'testing',
        }
    }
