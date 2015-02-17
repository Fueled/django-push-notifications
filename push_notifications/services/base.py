

class BaseService(object):

    def __init__(self, configuration):
        pass

    def send_push_notification(devices, message,
                               badge_number=None, sound=None,
                               payload=None, expiry=None):
        pass
