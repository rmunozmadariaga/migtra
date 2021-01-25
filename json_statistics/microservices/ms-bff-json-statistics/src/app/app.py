import logging
import pendulum
import os

from utils.utils import send_response, send_response_list

from flask import Flask, jsonify, json, request

app = Flask(__name__)

app.config['TIMEZONE'] = os.environ['TIMEZONE']

@app.route('/')
def index():
    return 'ok!'

@app.errorhandler(422)
def validation_error(err):
    messages = err.data.get('messages')
    if 'query' in messages:
        return send_response(messages.get('query'), 409)
    elif 'json' in messages:
        return send_response(messages.get('json'), 409)

@app.route("/average_var1", methods=['GET'])
def average_var1():
    try:

        suma_var1 = 0
        num_ciudades = 0

        data = request.json

        for x in range(0,len(data)):

            provincia = data[x]['children']

            for y in range (0,len(provincia)):

                ciudad = provincia[y]['children']

                for z in range (0,len(ciudad)):

                    var1 = ciudad[z]['values']['var1']
                    suma_var1 = suma_var1 + var1
                    num_ciudades = num_ciudades + 1

        average_var1 = suma_var1 / num_ciudades

        return send_response("Promedio VAR 1 es: " + str(average_var1), 200)

    except Exception as error:
        logging.exceptionI('Error en funcion average_var1')

        return send_response(error.args)


@app.route("/sum_var2_prov2", methods=['GET'])

def sum_var2_prov2():
    try:

        sum_var2_prov2 = 0

        data = request.json

        for x in range(0,len(data)):

            provincia = data[x]['children']

            for y in range (0,len(provincia)):

                nombre_provincia = provincia[y]['name']

                if nombre_provincia == 'Provincia2':

                    ciudad = provincia[y]['children']

                    for z in range (0,len(ciudad)):

                        var2 = ciudad[z]['values']['var2']
                        sum_var2_prov2 = sum_var2_prov2 + var2

        return send_response("Suma VAR 2 de Provincia2 es: " + str(sum_var2_prov2), 200)

    except Exception as error:
        logging.exceptionI('Error en funcion sum_var2_prov2')

        return send_response(error.args)

@app.route("/max_var1_reg4", methods=['GET'])
def max_var1_reg4():
    try:

        array_var1 = []

        data = request.json

        for x in range(0,len(data)):


            logging.info(data[x]['name'])
            nombre_region = data[x]['name']

            if nombre_region == 'Region4':
                provincia = data[x]['children']

                for y in range (0,len(provincia)):

                    ciudad = provincia[y]['children']

                    for z in range (0,len(ciudad)):

                        var1 = ciudad[z]['values']['var1']
                        array_var1.append(var1)

        max_var1_reg4 = max(array_var1)

        return send_response("Maximo VAR 1 de Region4 es: " + str(max_var1_reg4), 200)

    except Exception as error:
        logging.exceptionI('Error en funcion max_var1_reg4')

        return send_response(error.args)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
