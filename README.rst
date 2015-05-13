Django Push Notifications
=========================
.. image:: https://travis-ci.org/Fueled/django-push-notifications.svg
    :target: https://travis-ci.org/Fueled/django-push-notifications

This package makes it easy to support Push notifications. It works
together with third party services such as ``ZeroPush``.

You can easily add permissions to push devices by chaining those devices
to a notification setting. For registering a new push device you can add
custom permissions.

Installation
------------

To install the package on your machine you can run the PIP install:

::

    pip install django-pnm

Configuration
-------------

First you have to add ``push_notifications`` to your installed apps:

.. code:: python

      INSTALLED_APPS = (
        ...
        'push_notifications',
      )

To setup the package you have to add a ``DJANGO_PUSH_NOTIFICATIONS``
into your settings:

.. code:: python

    def Settings(Configuration):
      # ...
      DJANGO_PUSH_NOTIFICATIONS = {
          'SERVICE': 'push_notifications.services.zeropush.ZeroPushService',
          'AUTH_TOKEN': '123123123'
      }

The ``SERVICE`` Key can be set to the type of service you use. In this
example we use the ``ZeroPushService``. With the ``ZeroPush`` Service we
are required to add a ``AUTH_TOKEN`` to the ``Configuration``.


Don't forget to run the migrations
~~~~~~~~~~~~~~~
Then run the migrations by running: ``python manage.py migrate``


**Note**: Right now, only ``ZeroPush`` is available. More services will
be available soon.

For Django REST Framework users
-------------

There are also 2 endpoints for you available. These can be used to register and unregister a push device. The endpoints are Auth protected with the default settings of your Django REST Framework set up.

To enable the ``unregister`` and ``register`` endpoints you can add the following to your ``urls.py`` file:

.. code:: python
    url(r'^notifications/', include('push_notifications.urls')),


**Note**: We purposely have chosen to not include ``djangorestframework`` as a dependecy. If you don't have it you would have to include it in your ``requirements.txt`` file.

Usage
-----

Register a device
~~~~~~~~~~~~~~~~~

To register a new device you can use the ``register_push_device`` method
in ``utils``:

.. code:: python

    from push_notifications.utils from register_push_device

    token = "<The device token>"
    register_push_device(user, token)

You can also pass notification permissions directly to the
``register_push_device`` method:

.. code:: python

    register_push_device(user, token, ['likes', 'comments'])

Add permissions
~~~~~~~~~~~~~~~

To add an notification permission to a push device you can use the
``add_permission`` method on the ``device`` object:

.. code:: python

    device.add_permission('likes')

Or adding multiple permissions

.. code:: python

    device.add_permissions(['likes', 'comments'])

Add all the permission for the devices that the user owns.

.. code:: python

    user.push_devices.add_permissions(['likes', 'comments'])

Remove permissions
~~~~~~~~~~~~~~~~~~

To remove a notification permission you can use ``remove_permission``
method on the ``device`` object:

.. code:: python

    device.remove_permissions('likes')

Or removing multiple permissions

.. code:: python

    device.remove_permissions(['likes', 'comments'])

Remove all the permission for the devices that the user owns.

.. code:: python

    user.push_devices.remove_permissions(['likes', 'comments'])

Send a notification
~~~~~~~~~~~~~~~~~~~

To send a notification to a certain permission group you can call
``send_push_notification`` in ``utils``:

.. code:: python

    from push_notifications import send_push_notification
    from datetime import timedelta

    send_push_notification('likes', 'This is the message', sound="annoyingSound.mp3",
                                                           badge_number=1
                                                           info={
                                                            "extra": "payload",
                                                            "in": "notification"
                                                           },
                                                           expiry=timedelta(days=30))

Description
^^^^^^^^^^^

``send_push_notification(notify_type, message, **kwargs)``

**kwargs** - ``sound``: The sound that has to be played when sending the
notification - ``badge_number``: The badge\_number that has to be
displayed **(iOS Only)** - ``info``: Extra payload that comes along the
notification - ``expiry``: The expiry of the notification **Accepts
timedelta and datetime object**

Send a notification to one device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To send a notification to a specific device you can use the
``send_push_notification`` on the ``device`` object

.. code:: python

    device.send_push_notification('likes', 'This is the message', sound="annoyingSound.mp3",
                                                                  badge_number=1
                                                                  info={
                                                                    "extra": "payload",
                                                                    "in": "notification"
                                                                  },
                                                                  expiry=timedelta(days=30))

It accepts the same parameters as the global ``send_push_notification``
in ``utils``.

Send a notification to one user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To send a notification to a user and all its devices you can use the
``send_push_notification`` on the ``push_devices`` name in your user
object:

.. code:: python

    user.push_devices.send_push_notification('likes', 'This is the message',
                                             sound="annoyingSound.mp3",
                                             badge_number=1
                                             info={
                                               "extra": "payload",
                                               "in": "notification"
                                             },
                                             expiry=timedelta(days=30))
