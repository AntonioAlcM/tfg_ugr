
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,jsonify, redirect,url_for
from json import dumps
import celery , sys
from celery import Celery
from celery.result import AsyncResult
from Buscador import tasks
import time, json
app = Flask(__name__)

@app.route('/datos', methods=['GET', 'POST'])
def recibirInformacion():
    resultados=[]
    informacion = tratamientosDatos(json.loads(request.args.get('expedientes')),request.args.get('array'))
    resultados=informacion.unirVectores()
    return  jsonify(resultados)

class tratamientosDatos():
    def __init__(self, resultados_ncbi, resultados_array):
        self.datos_ncbi=resultados_ncbi[:]
        self.resultados_array=resultados_array
    def almacenar_datos_visualizacion_array(self):
        visualizacion_array=[]

        for i in AsyncResult(self.resultados_array).get()['experiments']['experiment']:
            visualizacion_array.append({'id': i['id'],
            'accession': i['accession'],
            'name': i['name'], 'releasedate': i['releasedate'],
             'description': i['description'][0]['text'],'bd': 'arrayexpress', 'descarga': "null"  })
        
        return visualizacion_array
    def almacenar_datos_visualizacion_ncbi(self):
        tam_list=len(self.datos_ncbi)
        visualizacion_ncbi=[]
        for i in self.datos_ncbi:
            identificador=AsyncResult(i).get()['result']['uids'][0]
            visualizacion_ncbi.append({'id': identificador,
            'accession': AsyncResult(i).get()['result'][identificador]['accession'],
             'name':  AsyncResult(i).get()['result'][identificador]['title'],
              'releasedate': AsyncResult(i).get()['result'][identificador]['pdat'],
               'description':  AsyncResult(i).get()['result'][identificador]['summary'],
               'bd': 'ncbi_gds', 'descarga': AsyncResult(i).get()['result'][identificador]['ftplink']})
        return visualizacion_ncbi

    def unirVectores(self):
        vector_ncbi=[]
        vector_array=[]
        vector_ncbi=self.almacenar_datos_visualizacion_ncbi()
        vector_array=self.almacenar_datos_visualizacion_array()
        for i in vector_array:
            vector_ncbi.append(i)
        return vector_ncbi

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
