from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.http import JsonResponse
from django.core import serializers
import json, time, requests, urllib, os, re, math
from ftplib import FTP
from json import dumps
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
#from Buscador.tasks import obtenerJson, obtenerJsonArray, devolverExpedientes
from Buscador.tasks import obtenerJson
from BuscadorBDMedical.celery import app as app
from django.views.decorators.csrf import csrf_exempt
regex_hg = r"((hg[0-9][0-9]))"
regex_grch = r"((grch[0-9][0-9]))"
regex_grcm = r"((grcm[0-9][0-9]))"


@csrf_exempt
def cargarPaginaBusqueda(request):
    resultados_busqueda = json.loads(request.POST['myInput'])
    ncbi = app.AsyncResult(resultados_busqueda['ncbi'])
    array = app.AsyncResult(resultados_busqueda['array'])
    busqueda=Buscador()
    expedientes = busqueda.obtenerExpedientes(ncbi)
    informacion = TratamientosDatos(expedientes, array)
    lista = []
    lista = informacion.unirVectores()
    context = {"coincidencias": json.dumps(lista), "total_casos_ncbi": ncbi.get()['esearchresult']['retmax'], "total_casos_array": array.get()[
        'experiments']['total'], "busqueda": resultados_busqueda['busqueda']}
    return render(request, 'listarBusqueda.html', context)

'''
def obtenerExpedientes(resultados_busqueda):
    resultados_ncbi = []
    resultados_array = []
    resultados = []
    if int(resultados_busqueda.get()['esearchresult']['count']) < 2:
        for i in range(0, int(resultados_busqueda.get()['esearchresult']['count']), 500):
            url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&query_key=1&WebEnv={}&retstart={}&retmax=500&rettype=json&retmode=json'.format(
                resultados_busqueda.get()['esearchresult']['webenv'], i)
            ncbi_uids = obtenerJson.apply_async(kwargs={'url': url})
            resultados.append(ncbi_uids)
        return resultados
    else:
        resultados_ncbi = devolverExpedientes.apply_async(kwargs={'inicio': 0, 'fin': round(int(resultados_busqueda.get(
        )['esearchresult']['count'])/2), 'cola': "ncbi", 'resultados_busqueda': resultados_busqueda.get()['esearchresult']['webenv']})
        resultados_array = devolverExpedientes.apply_async(kwargs={'inicio': math.ceil(int(resultados_busqueda.get()['esearchresult']['count'])/2), 'fin': int(
            resultados_busqueda.get()['esearchresult']['count']), 'cola': "Array", 'resultados_busqueda': resultados_busqueda.get()['esearchresult']['webenv']})
        for elements in resultados_ncbi.get():
            resultados.append(app.AsyncResult(elements))
        for elements in resultados_array.get():
            resultados.append(app.AsyncResult(elements))
        return resultados
'''

class Buscador(object):
    def __init__(self):
        self.resultados = []
    def obtenerExpedientes(self,resultados_busqueda):
        for i in range(0,int(resultados_busqueda.get()['esearchresult']['count']),500):
            url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&query_key=1&WebEnv={}&retstart={}&retmax=500&rettype=json&retmode=json'.format(resultados_busqueda.get()['esearchresult']['webenv'],i)
            '''
            response = urlopen(url)
            ncbi_uids = json.loads(response.read().decode('utf-8'))
            '''
            ncbi_uids = obtenerJson.apply_async(kwargs={'url': url})
            self.resultados.append(ncbi_uids)
        return self.resultados



class TratamientosDatos():
    def __init__(self, resultados_ncbi, resultados_array):
        self.datos_ncbi = resultados_ncbi[:]
        self.resultados_array = resultados_array

    def almacenar_datos_visualizacion_array(self):
        visualizacion_array = []
        for i in self.resultados_array.get()['experiments']['experiment']:
            if 'experimenttype' in i:
                tipoexperimento = i['experimenttype'][0]
            else:
                tipoexperimento = '\xa0Information not available'
            if 'bioassaydatagroup' in i:
                for j in i['bioassaydatagroup']:
                    if 'scan' in j['name']:
                        samples = j['bioassaydatacubes']
                    elif 'rawdata' in j['name']:
                        samples = j['bioassaydatacubes']
                    elif 'normalization' in j['name'] and 'processedData' in j['name']:
                        samples = j['bioassaydatacubes']*2
                    else:
                        samples = '\xa0There are no samples'
            else:
                samples = '\xa0There are no samples'
            visualizacion_array.append({'id': i['id'],
                                        'accession': i['accession'],
                                        'name': i['name'], 'releasedate': i['releasedate'].replace("-", "/"),
                                        'description': i['description'][0]['text'], 'bd': 'ArrayExpress',
                                        'descarga': "https://www.ebi.ac.uk/arrayexpress/experiments/{}/files/".format(i['accession']),
                                        'especie': i['organism'][0], 'tipoexperimento': tipoexperimento,
                                        'n_samples': samples})
        return visualizacion_array

    def almacenar_datos_visualizacion_ncbi(self):
        visualizacion_ncbi = []
        for i in self.datos_ncbi:
            if 'result' in i.get():
                for j in i.get()['result']['uids']:
                    if i.get()['result'][j]['gdstype'] != "":
                        tipoexperimento = i.get()['result'][j]['gdstype']
                    else:
                        tipoexperimento = '\xa0Information not available'
                    if i.get()['result'][j]['n_samples'] != "":
                        muestras = i.get()['result'][j]['n_samples']
                    else:
                        muestras = '\xa0There are no samples'
                    visualizacion_ncbi.append({'id': j,
                                            'accession': i.get()['result'][j]['accession'],
                                            'name':  i.get()['result'][j]['title'],
                                            'releasedate': i.get()['result'][j]['pdat'],
                                            'description':  i.get()['result'][j]['summary'],
                                            'bd': 'NCBI', 'descarga': i.get()['result'][j]['ftplink'],
                                            'especie': i.get()['result'][j]['taxon'],
                                            'tipoexperimento': tipoexperimento,
                                            'n_samples': muestras, 'samples': i.get()['result'][j]['samples']})
        return visualizacion_ncbi

    def unirVectores(self):
        vector_busqueda = []
        if len(self.datos_ncbi) > 0:
            vector_busqueda = self.almacenar_datos_visualizacion_ncbi()
            if self.resultados_array.get()['experiments']['total'] > 0:
                for i in self.almacenar_datos_visualizacion_array():
                    vector_busqueda.append(i)
        elif self.resultados_array.get()['experiments']['total'] > 0:
            vector_busqueda = self.almacenar_datos_visualizacion_array()
        return vector_busqueda


'''
def descargaDeContenido(request):
    if request.method == 'POST':
        enlace=request.POST['enlace']
        direccion=enlace.split('//',1)
        direccion_cortada=direccion[1].split('/',1)
        direccion_servidor=direccion_cortada[1].split('/',7)
        ftp = FTP(direccion_cortada[0])
        ftp.login()
        direccion=direccion_servidor[0]+"/"+direccion_servidor[1]+"/"+direccion_servidor[2]+"/"+direccion_servidor[3]+"/"+direccion_servidor[4]+"/"+direccion_servidor[5]+"/"+direccion_servidor[6]
        ftp.cwd(direccion)
        dirs=ftp.nlst()
        for i in dirs:
            ftp.retrbinary('RETR %s' % os.path.basename(j),file_handler)#La recepción
            archivo = eg.filesavebox(title="Guardar",default=j)
            tam=archivo.count('/')
            ruta_guardado=""
            for rut in archivo.split('/',tam):
                ruta_guardado+='/'
                ruta_guardado+=rut
            ftp.retrbinary('RETR '+j, open('~/', 'wb').write)
        ftp.quit()
        return JsonResponse('ok', safe=False)
'''
# def busqueda_avanzada(palabra_clave, tecnologia_secuenciacion,localizacion, organismo, base_datos):
#	if (base_datos=="ncbi"):


@csrf_exempt
def inicializarBuscador(request):
    if request.method == "POST":
        palabra_clave = request.POST['search']
        palabra_clave = palabra_clave.replace(' ', '%20')
        url_ncbi = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term={}&datetype=edat&retmax=10000000&usehistory=y&retmode=json'.format(
            palabra_clave)
        url_array = 'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments?keywords={}'.format(
            palabra_clave)
        data_ncbi = obtenerJson.apply_async(kwargs={'url': url_ncbi})
        data_array = obtenerJson.apply_async(kwargs={'url': url_array})
        cnt = 0
        while data_array.status == 'PENDING' and cnt < 3:
            time.sleep(0.2)
            cnt += 1
        if data_ncbi.get()['esearchresult']['retmax'] == '0' and cnt == 2:
            return render(request, 'NoResults.html')
        else:
            context = {"enlaces_busqueda": [
                data_ncbi, data_array], "busqueda": request.POST['search']}
            return render(request, 'loader.html', context)
    else:
        return render(request, 'index.html')


@csrf_exempt
def inicializarBuscadorGSE(request):
    if request.method == "POST":
        palabra_clave = request.POST['search']
        palabra_clave = palabra_clave.replace(' ', '%20')
        url_ncbi = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=GSE+{}&datetype=edat&retmax=10000000&usehistory=y&retmode=json'.format(
            palabra_clave)
        url_array = 'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments?keywords={}'.format(
            palabra_clave)
        data_ncbi = obtenerJson.apply_async(kwargs={'url': url_ncbi})
        data_array = obtenerJson.apply_async(kwargs={'url': url_array})
        cnt = 0
        while data_array.status == 'PENDING' and cnt < 3:
            time.sleep(0.2)
            cnt += 1
        if data_ncbi.get()['esearchresult']['retmax'] == '0' and cnt == 2:
            return render(request, 'NoResults.html')
        else:
            context = {"enlaces_busqueda": [
                data_ncbi, data_array], "busqueda": request.POST['search']}
            return render(request, 'loader.html', context)
    else:
        return render(request, 'index.html')


@csrf_exempt
def sendFile(request):
    searched_file = json.loads(request.POST['myInput'])
    genome = []
    if searched_file['file']['bd'] == 'ArrayExpress':
        # file=obtenerJson.apply_async(kwargs={'url':'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments/{}'.format(searched_file['accession'])})
        muestras = obtenerJson.apply_async(
            kwargs={'url': 'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments/{}/samples/'.format(searched_file['accession'])})
        archivo = urlopen(searched_file['file']['descarga'] +
                          searched_file['file']['accession']+'.idf.txt').readlines()
        for i in archivo:
            if i:
                if re.findall(regex_hg, i.decode('utf-8', errors="ignore").lower()):
                    genome.append(re.findall(regex_hg, i.decode(
                        'utf-8', errors="ignore").lower())[0][0])
                if re.findall(regex_grch, i.decode('utf-8', errors="ignore").lower()):
                    genome.append(re.findall(regex_grch, i.decode(
                        'utf-8', errors="ignore").lower())[0][0])
                    print(re.findall(regex_grch, i.decode(
                        'utf-8', errors="ignore").lower())[0][0])
                if re.findall(regex_grcm, i.decode('utf-8', errors="ignore").lower()):
                    genome.append(re.findall(regex_grcm, i.decode(
                        'utf-8', errors="ignore").lower())[0][0])
        if genome:
            genome = set(genome)
        else:
            genome.append("Not Available")
        searched_file['file'].update(
            {'samples': muestras.get()['experiment']['sample']})
        searched_file['file'].update(
            {'n_samples': len(muestras.get()['experiment']['sample'])})
        searched_file['file'].update({'genome': genome})
        context = {"file": searched_file['file']}
        return render(request, 'expedient.html', context)
    else:
        if searched_file['file']:
            archivo = urlopen('https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' +
                              searched_file['file']['samples'][0]['accession']).readlines()
            for i in archivo:
                if i:
                    if re.findall(regex_hg, i.decode('utf-8', errors="ignore").lower()):
                        genome.append(re.findall(regex_hg, i.decode(
                            'utf-8', errors="ignore").lower())[0][0])
                    if re.findall(regex_grch, i.decode('utf-8', errors="ignore").lower()):
                        genome.append(re.findall(regex_grch, i.decode(
                            'utf-8', errors="ignore").lower())[0][0])
                    if re.findall(regex_grcm, i.decode('utf-8', errors="ignore").lower()):
                        genome.append(re.findall(regex_grcm, i.decode(
                            'utf-8', errors="ignore").lower())[0][0])
            if genome:
                genome = set(genome)
            else:
                genome.append("Not Available")
        context = {"file": searched_file['file']}
        searched_file['file'].update({'genome': genome})
        return render(request, 'expedient.html', context)


def index(request):
    return render(request, 'index.html')
