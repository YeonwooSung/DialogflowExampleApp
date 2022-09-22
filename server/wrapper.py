from flask import Response
from functools import wraps
import json


def as_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = f(*args, **kwargs)
        return Response(json.dumps(data), mimetype='application/json; charset=utf-8')
    return wrapper