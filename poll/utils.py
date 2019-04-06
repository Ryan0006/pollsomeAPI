from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
import json
import uuid
import datetime


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return obj


def httpResponseNotFound(message):
    returned = {}
    returned["error"] = message
    return HttpResponseNotFound(json.dumps(returned), content_type="application/json")


def httpResponseBadRequest(message):
    returned = {}
    returned["error"] = message
    return HttpResponseBadRequest(json.dumps(returned), content_type="application/json")


def httpResponse(data):
    returned = {}
    returned["data"] = data
    return HttpResponse(json.dumps(data, cls=Encoder), content_type="application/json")
