import os
import base64
import psycopg2
import psycopg2.extras
from os import environ
import logging


loglevels = {
    'INFO': logging.INFO,
    'ERROR': logging.ERROR,
    'DEBUG': logging.DEBUG
}

LOG_LEVEL = logging.INFO
if environ.get('LOG_LEVEL') is not None:
    LOG_LEVEL = loglevels[environ.get('LOG_LEVEL')]

logging.basicConfig(level=LOG_LEVEL)
"""
deprecado
"""
def connect_db(app):
    """
    Crea conexión con DB
    """

    db_host = os.environ['HOST']
    db_database = os.environ['DATABASE']
    db_username = 'postgres'
    db_password = os.environ['PASSWORD']

    connection = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_username,
        password=db_password,
        cursor_factory=psycopg2.extras.DictCursor
    )

    return connection




class db_manager(object):

    key_values = [ 'HOST', 'PASSWORD', 'DATABASE','USERNAME']

    def __init__(self, params):
        self._connection = None

        result = [ x for x in params.keys() if x not in self.key_values ]

        if len(result) > 0:
            raise Exception(f'Faltan los siguientes valores: {result}')

        logging.info('Inicializando administrador de conexiones')
        self.db_host = params['HOST']
        self.db_database = params['DATABASE']
        self.db_username = params['USERNAME']
        self.db_password = params['PASSWORD']

    def __enter__(self):

        try:

            if self._connection is None:
                self._connection = psycopg2.connect(
                    host=self.db_host,
                    database=self.db_database,
                    user=self.db_username,
                    password=self.db_password,
                    cursor_factory=psycopg2.extras.DictCursor
                )
                self._connection.autocommit = True

            else:
                logging.info('Retornando conexión abierta')

        except:
            logging.exception('Error al crear la conexion de base de datos')
            raise
        else:
            logging.debug('Retornando conexión')
            return self._connection


    def __exit__(self, type, value, traceback):
        try:
            if self._connection is not None:
                self._connection.close()
                self._connection = None
            else:
                logging.warning('')
        except:
            logging.exception('Error al cerrar la conexion de base de datos')
        else:
            logging.info('La conexión se ha cerrado correctamente')
