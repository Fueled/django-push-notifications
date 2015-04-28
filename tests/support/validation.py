import six
from datetime import datetime


def validate_zeropush_payload(payload, expiry_check=datetime.now()):
    """
    All the validation is according to the payload description
    described here: https://zeropush.com/documentation/api_reference#notify
    """

    # We need to do this because querystrings are not really well parsed
    device_tokens = payload['device_tokens']['']
    assert len(device_tokens) > 0

    if 'alert' in payload:
        # Payload is optional
        assert isinstance(payload['alert'], six.string_types)
        assert payload['alert'] != ""

    if 'badge' in payload:
        assert isinstance(payload['badge'], six.string_types) or isinstance(payload['badge'], six.integer_types)

    if 'sound' in payload:
        assert isinstance(payload['sound'], six.string_types)

    if 'expiry' in payload:
        assert type(payload['expiry']) is int

    return True
