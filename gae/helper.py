# from http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models
import datetime
import json
import time

from google.appengine.ext import ndb

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_json(obj):
    if obj is None or isinstance(obj, SIMPLE_TYPES):
        pass
    elif type(obj) is ndb.Key:
        obj = str(obj.id())
    else:
        obj = to_dict(obj)

    return json.dumps(obj)

def to_dict(model):
    output = {}

    for key, prop in model.to_dict().items():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to ms-since-epoch ("new Date()").
            ms = time.mktime(value.utctimetuple())
            ms += getattr(value, 'microseconds', 0) / 1000
            output[key] = int(ms)
        elif isinstance(value, ndb.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, ndb.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output