import logging
import pendulum
import os

from utils.utils import send_response

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

@app.route("/avg_wait_time", methods=['GET'])
def avg_wait_time():
    try:

        data = request.json

        num_reg = len(data)

        array_ae = []
        array_be = []

        for x in range(0,num_reg):

            zone = data[x]['zone']

            if zone == 'AE1' or zone == 'AE2':

                dt_in = data[x]['dt_in']
                dt_out = data[x]['dt_out']

                t_out = pendulum.parse(dt_out)
                t_in = pendulum.parse(dt_in)

                wait_minutes = t_out.diff(t_in).in_minutes()

                array_ae.append(wait_minutes)

            elif zone == 'BE1' or zone == 'BE2':

                dt_in = data[x]['dt_in']
                dt_out = data[x]['dt_out']

                t_out = pendulum.parse(dt_out)
                t_in = pendulum.parse(dt_in)

                wait_minutes = t_out.diff(t_in).in_minutes()

                array_be.append(wait_minutes)

        avg_ae = round(sum(array_ae) / len(array_ae),2)
        avg_be = round(sum(array_be) / len(array_be),2)

        return send_response("Promedio de tiempo de espera en zona A es de " + str(avg_ae) + " minutos y en zona B es de "+ str(avg_be) + " minutos", 200)

    except Exception as error:
        logging.exceptionI('Error en funcion avg_wait_time')

        return send_response(error.args)

@app.route("/aw2_bw2", methods=['GET'])
def aw2_bw2():
    try:

        data = request.json

        work_zone = 0
        num_reg = len(data)

        for x in range(0,num_reg):

            zone = data[x]['zone']

            if zone == 'AW2' or zone == 'BW2':

                work_zone += 1

        quotient = work_zone / num_reg

        percentage_aw2_bw2 = round(quotient * 100, 2)

        return send_response("Porcentaje ciclos de faena que incluyeron algun área de trabajo tipo 2 es: " + str(percentage_aw2_bw2) + "%", 200)

    except Exception as error:
        logging.exceptionI('Error en funcion aw2_bw2')

        return send_response(error.args)

@app.route("/aw1_aw2_vs_bw1_bw2", methods=['GET'])
def aw1_aw2_vs_bw1_bw2():
    try:

        data = request.json

        work_zone_aw1 = 0
        work_zone_aw2 = 0
        work_zone_bw1 = 0
        work_zone_bw2 = 0
        num_reg = len(data)

        for x in range(0,num_reg):

            zone = data[x]['zone']

            if zone == 'AW1' or zone == 'AW2':

                if zone == 'AW1':

                    work_zone_aw1 += 1

                elif zone == 'AW2':

                    work_zone_aw2 += 1

            if zone == 'BW1' or zone == 'BW2':

                if zone == 'BW1':

                    work_zone_bw1 += 1

                elif zone == 'BW2':

                    work_zone_bw2 += 1

        recap_work = { "AW1": work_zone_aw1, "AW2": work_zone_aw2, "BW1": work_zone_bw1, "BW2": work_zone_bw2}

        recap_aw_bw = { "AW": work_zone_aw1 + work_zone_aw2, "BW": work_zone_bw1 + work_zone_bw2}

        max_work_value = max(recap_work.values())
        max_work_key = max(recap_work, key=recap_work.get)

        max_work_aw_bw_value = max(recap_aw_bw.values())
        max_work_aw_bw_key = max(recap_aw_bw, key=recap_aw_bw.get)

        quotient_aw_bw = max_work_aw_bw_value / num_reg

        percentage_aw_bw = round(quotient_aw_bw * 100, 2)

        return send_response("La zona de trabajo con mayor demanda es "+ str(max_work_key) + " con una cantidad de " + str(max_work_value) + " de operaciones registradas y en suma global de trabajo la zona mas utilizada es " + str(max_work_aw_bw_key) + " con una cantidad total de " + str(max_work_aw_bw_value) + " operaciones (" + str(percentage_aw_bw)+ "% de total registrado)", 200)

    except Exception as error:
        logging.exceptionI('Error en funcion aw1_aw2_vs_bw1_bw2')

        return send_response(error.args)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
