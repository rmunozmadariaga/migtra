import io
import os
import csv
import json
from flask import jsonify
from decimal import Decimal
from datetime import datetime


JSON_MIMETYPE='application/json'


def default(obj):
    """
    Transforma los items de tipo "Decimal" & "datetime" a string.

    PD: Se pueden agregar mas tipos.
    """
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, datetime):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def send_response_list(app, data, status_code = 200):
    return app.response_class(
        response=data,
        status=status_code,
        mimetype='application/json',
        headers = {'Access-Control-Allow-Origin': '*', 'Content-Type': JSON_MIMETYPE}
    )

def send_response(error, status_code = 500):
    response = jsonify({'code': status_code, 'message': error})
    response.status_code = status_code
    response.mimetype = 'application/json'
    response.headers = {'Access-Control-Allow-Origin': '*', 'Content-Type': JSON_MIMETYPE}

    return response
