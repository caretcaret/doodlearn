# from http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models
import datetime
import json
import time

from google.appengine.ext import ndb
import logging

SIMPLE_TYPES = (int, long, float, bool, dict, basestring)

def slice_grouper(n, sequence):
   return [sequence[i:i+n] for i in range(0, len(sequence), n)]

def key_results(l):
    result = {}
    for item in l:
        result[item.key] = item
    return result

def unkey_results(d):
    return [v for (k,v) in d.items()]

def to_json(obj):
    return json.dumps(to_dict(obj))

def to_dict(model):
    if model is None or isinstance(model, SIMPLE_TYPES):
        return model
    elif type(model) is ndb.Key:
        return str(model.id())
    elif type(model) is list:
        return map(to_dict, model)
    elif isinstance(model, datetime.date):
        # Convert date/datetime to ms-since-epoch ("new Date()").
        ms = time.mktime(value.utctimetuple())
        ms += getattr(model, 'microseconds', 0) / 1000
        return int(ms)
    elif isinstance(model, ndb.GeoPt):
        return {'lat': model.lat, 'lon': model.lon}
    elif isinstance(model, ndb.Model):
        output = {}

        for key, prop in model.to_dict().items():
            value = getattr(model, key)

            output[key] = to_dict(value)

        output['id'] = to_dict(model.key)

            

        return output
    else:
        raise ValueError('cannot encode ' + repr(prop))
