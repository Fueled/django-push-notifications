# Django Push Notifications

This package makes it easy to support Push notifications. It works together with third party services such as `ZeroPush`.

You can easily add permissions to push devices by chaining those devices to a notification setting. For registering a new push device you can add custom permissions.

## Configuration
__TODO__

## Usage

### Register a device
To register a new device you can use the `register_push_device` method in `utils`:
```python
from push_notifications.utils from register_push_device

token = "<The device token>"
register_push_device(user, token)
```

You can also pass notification permissions directly to the `register_push_device` method:
```python
register_push_device(user, token, ['likes', 'comments'])
```

### Add permissions
To add an notification permission to a push device you can use the `add_permission` method on the `device` object:
```python
device.add_permission('likes')
```

Or adding multiple permissions
```python
device.add_permissions(['likes', 'comments'])
```

Add all the permission for the devices that the user owns.
```python
user.push_devices.add_permissions(['likes', 'comments'])
```

### Remove permissions
To remove a notification permission you can use `remove_permission` method on the `device` object:
```python
device.remove_permissions('likes')
```

Or removing multiple permissions
```python
device.remove_permissions(['likes', 'comments'])
```

Remove all the permission for the devices that the user owns.
```python
user.push_devices.remove_permissions(['likes', 'comments'])
```

### Send a notification
To send a notification to a certain permission group you can call `send_push_notification` in `utils`:
```python
from push_notifications import send_push_notification
from datetime import timedelta

send_push_notification('likes', 'This is the message', sound="annoyingSound.mp3",
                                                       badge_number=1
                                                       info={
                                                        "extra": "payload",
                                                        "in": "notification"
                                                       },
                                                       expiry=timedelta(days=30))
```

#### Description
`send_push_notification(notify_type, message, **kwargs)`

**kwargs**
- `sound`: The sound that has to be played when sending the notification
- `badge_number`: The badge_number that has to be displayed __(iOS Only)__
- `info`: Extra payload that comes along the notification
- `expiry`: The expiry of the notification __Accepts timedelta and datetime object__

### Send a notification to one device
To send a notification to a specific device you can use the `send_push_notification` on the `device` object

```python
device.send_push_notification('likes', 'This is the message', sound="annoyingSound.mp3",
                                                              badge_number=1
                                                              info={
                                                                "extra": "payload",
                                                                "in": "notification"
                                                              },
                                                              expiry=timedelta(days=30))
```
It accepts the same parameters as the global `send_push_notification` in `utils`.

### Send a notification to one user
To send a notification to a user and all its devices you can use the `send_push_notification` on the `push_devices` name in your user object:

```python
user.push_devices.send_push_notification('likes', 'This is the message',
                                         sound="annoyingSound.mp3",
                                         badge_number=1
                                         info={
                                           "extra": "payload",
                                           "in": "notification"
                                         },
                                         expiry=timedelta(days=30))
```


