
from .models import PushDevice


def register_push_device(user, token, notice_types=None):
    return PushDevice.register_push_device(user, token, notice_types)
