# -*- coding: utf-8 -*-
import json

# Third party
from django.http import HttpResponse

# Local
from .forms import PushDeviceForm
from .models import PushDevice


def _user_not_authenticated_response():
    return _send_response(
        {'detail': 'There is no user authenticated'},
        status_code=403)


def _method_not_supported_response(request):
    return _send_response(
        {'detail': '{} method not supported'.format(request.method)},
        status_code=503)


def _send_response(json_response, status_code=200, **kwargs):
    response = HttpResponse(json.dumps(json_response),
                            content_type="application/json", **kwargs)
    response.status_code = status_code
    return response


def unregister_device(request):
    """
    Unregister device of Pushdevices
    """
    if not hasattr(request, 'user'):
        return _user_not_authenticated_response()
    elif not request.user.is_authenticated():
        return _user_not_authenticated_response()

    # Check if there is payload
    if request.method == 'POST':
        form = PushDeviceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            PushDevice.unregister_push_device(request.user,
                                              form.cleaned_data['token'])
            return _send_response({'unregistered': True}, status_code=200)

        # Return back errors
        data = {
            'unregistered': False
        }
        data.update(form.errors)
        return _send_response(data, status_code=400)

    # Send back response that method is not supported
    return _method_not_supported_response(request)


def register_device(request):
    """
    Register device of Pushdevices
    """
    if not hasattr(request, 'user'):
        return _user_not_authenticated_response()
    elif not request.user.is_authenticated():
        return _user_not_authenticated_response()

    # Check if there is payload
    if request.method == 'POST':
        form = PushDeviceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            PushDevice.register_push_device(request.user,
                                            form.cleaned_data['token'])
            return _send_response({'registered': True}, status_code=200)

        # Return back errors
        data = {
            'registered': False
        }
        data.update(form.errors)
        return _send_response(data, status_code=400)

    # Send back response that method is not supported
    return _method_not_supported_response(request)
