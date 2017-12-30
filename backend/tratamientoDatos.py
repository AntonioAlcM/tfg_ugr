
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,jsonify, redirect,url_for
from json import dumps
import celery , sys
from celeryconfig import appcelery
from Buscador import tasks
import time, json
app = Flask(__name__)

@app.route('/datos', methods=['GET', 'POST'])
def recibirInformacion():
    resultados=[]
    expedientes=[]
    expedientes=convertirAstring(request.args.get('expedientes'))
    informacion = tratamientosDatos(expedientes,request.args.get('array'))
    resultados=informacion.unirVectores()
    return  jsonify(resultados)

def convertirAstring(argumentos):
    argumentos=argumentos.replace(' ','')
    argumentos=argumentos.replace('"','')
    argumentos=argumentos.replace(']','')
    argumentos=argumentos.replace('[','')
    argumentos=argumentos.split(',',argumentos.count(','))
    return argumentos

class tratamientosDatos():
    def __init__(self, resultados_ncbi, resultados_array):
        self.datos_ncbi=resultados_ncbi[:]
        self.resultados_array=resultados_array
    def almacenar_datos_visualizacion_array(self):
        visualizacion_array=[]
        for i in appcelery.AsyncResult(self.resultados_array).get()['experiments']['experiment']:
            visualizacion_array.append({'id': i['id'],
            'accession': i['accession'],
            'name': i['name'], 'releasedate': i['releasedate'],
             'description': i['description'][0]['text'],'bd': 'arrayexpress', 'descarga': "null"  })
        
        return visualizacion_array
    def almacenar_datos_visualizacion_ncbi(self):
        tam_list=len(self.datos_ncbi)
        visualizacion_ncbi=[]
        for j in range(tam_list):
            i=appcelery.AsyncResult(self.datos_ncbi[j])
            identificador=i.get()['result']['uids'][0]
            visualizacion_ncbi.append({'id': identificador,
            'accession':i.get()['result'][identificador]['accession'],
             'name':  i.get()['result'][identificador]['title'],
              'releasedate': i.get()['result'][identificador]['pdat'],
               'description':  i.get()['result'][identificador]['summary'],
               'bd': 'ncbi_gds', 'descarga': i.get()['result'][identificador]['ftplink'] })
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
