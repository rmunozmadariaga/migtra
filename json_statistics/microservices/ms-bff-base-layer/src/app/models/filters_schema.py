import re
import pendulum
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError

def validate_year_range(value):
    minimum = pendulum.datetime(2008, 1, 1 , tz='America/Santiago').format('YYYY')
    maximum = pendulum.now('America/Santiago').format('YYYY')

    if int(minimum) > value or int(maximum) < value:
        raise ValidationError("Debe ser menor que {} y mayor que {}".format(minimum, maximum))

def validate_month(value):
    minimum = 1
    maximum = 12
    if minimum > value or maximum < value:
        raise ValidationError("Debe ser menor que {} y mayor que {}".format(minimum, maximum))

def validate_date_format(value):
    regex = re.compile('\d{4}([-/])\d{2}([-/])\d{2}')
    if regex.match(value) is None:
        raise ValidationError("La debe poseer un formato valido (YYYY-MM-DD) ó (YYYY/MM/DD)")

class FiltersSchema(Schema):

    page = fields.Integer(validate=lambda val: val > 0, error_messages={
        'validator_failed': 'Número de pagina no puede ser menor a cero'
    })
    date_end = fields.String(validate=validate_date_format)
    date_init = fields.String(validate=validate_date_format)
    company = fields.String()
    month = fields.Integer(validate=validate_month)
    year = fields.Integer(validate=validate_year_range)
