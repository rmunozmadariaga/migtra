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

def psycopg2_array_to_json(rows):
    """
    Transforma el resultado de una consulta SQL
        [Decimal('1'), Decimal('1')]
    y lo transforma en un JSON
        [{"key": "value"}]
    """
    arr = []

    for row in rows:
        arr.append(dict(row))

    return json.dumps(arr, default=default)



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

def crear_archivo_s3(client, file_name, folder_s3, data, **know_args):
    if file_name == '':
        raise Exception('Nombre de archivo no puede ser vacio.')
    if folder_s3 == '':
        raise Exception('Carpeta destino no puede ser vacio.')
    if data == '':
        raise Exception('Data no puede ser vacio.')

    # If exists invalid fields then create error file
    if 'invalid' in know_args:
        # Updated folder to upload files
        folder_s3 = 'errores/{}'.format(folder_s3)

        # Create an "in memory" file for upload to s3
        output_file_invalid = io.StringIO()
        output = csv.writer(output_file_invalid)

        # Add row value to file
        for idx, item in enumerate(know_args.get('invalid')):
            if idx == 0:
                output.writerow(know_args.get('invalid')[0].keys())
            output.writerow(item.values())

        # Get content file
        contents_invalid = output_file_invalid.getvalue()

        output_file_invalid.close()

        # create file name for invalid items
        file_name_split = file_name.split('.')
        file_name_error = '{}_errores.{}'.format(file_name_split[0], file_name_split[1])

        # Upload file to bucket S3
        client.put_object(
            Body=contents_invalid,
            Bucket=os.environ['BUCKET_NAME'],
            Key='{}/{}'.format(folder_s3, file_name_error)
        )

    # Create an "in memory" file for upload to s3
    output_file = io.StringIO()
    output = csv.writer(output_file)

    # Add row value to file
    for idx, item in enumerate(data):
        if idx == 0:
            output.writerow(data[0].keys())
        output.writerow(item.values())

    # Get content file
    contents = output_file.getvalue()

    output_file.close()

    # Upload file to bucket S3
    client.put_object(
        Body=contents,
        Bucket=os.environ['BUCKET_NAME'],
        Key='{}/{}'.format(folder_s3, file_name)
    )
