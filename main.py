# chat conversation
import json
import pymysql
import requests
import http.client
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from itertools import cycle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["POST"])
@cross_origin()
def function(self):
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_DDBB = os.getenv("DB_DDBB")
    #try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DDBB)
    cursor = connection.cursor()

    print("conexión exitosa")

    sql = '''
    SELECT eu.usuario_id, e.nombre, e.apellido, es.especialidad
    FROM '''+DB_DDBB+'''.especialidad_user AS eu
    JOIN '''+DB_DDBB+'''.especialidades AS es ON eu.id_especialidad = es.id
    JOIN '''+DB_DDBB+'''.usuarios AS e ON eu.usuario_id = e.id
    WHERE eu.usuario_id = '''+str(request.json['usuario_id'])+''';
    '''
    
    cursor.execute(sql)
    resp = cursor.fetchall()
    print(str(resp))

    arrayEsp=[]
    retorno = {
        "especialidad":{}
    }
    for registro in resp:
        item={
            "usuario_id":registro[0],
            "nombre":registro[1],
            "apellido":registro[2],
            "especialidad":registro[3]
        }
        arrayEsp.append(item)
    retorno['especialidad'] = arrayEsp
    return retorno

    #except Exception as e:
    #    print('Error: '+ str(e))
    #    retorno = {           
    #        "detalle":"algo falló", 
    #        "validacion":False
    #    }
    #    return retorno

if __name__ == "__main__":
    app.run(debug=True, port=8002, ssl_context='adhoc')