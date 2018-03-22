from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json, requests, urllib, time, os
from ftplib import FTP
from json import dumps
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from Buscador.tasks import obtenerJson
from django.views.generic import View
from django.db import models

class buscador(View):
    def __init__(self):
        self.data_ncbi={}
        self.data_array={}
        self.palabra_clave=""
        self.url_ncbi=""
        self.url_array=""
        self.historial_busqueda=[]
        self.expedientes=[]
    def reiniciarBusqueda(self):
        self.data_ncbi={}
        self.data_array={}
        self.palabra_clave=""
        self.url_ncbi=""
        self.url_array=""
        self.expedientes=[]
    def buscar(self,request):
        self.reiniciarBusqueda()
        if request.method == "POST":
            self.palabra_clave=request.POST['search']
            self.palabra_clave=self.palabra_clave.replace(' ','%20')
            self.url_ncbi = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term={}&datetype=edat&retmax=10000000&usehistory=y&retmode=json'.format(self.palabra_clave)
            self.url_array = 'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments?keywords={}'.format(self.palabra_clave)
            self.data_ncbi=obtenerJson.apply_async(kwargs={'url': self.url_ncbi})
            self.data_array = obtenerJson.apply_async(kwargs={'url': self.url_array})
            self.historial_busqueda.append(self.data_ncbi)
            self.historial_busqueda.append(self.data_array)
            for i in range(0,int(self.data_ncbi.get()['esearchresult']['count']),500):
                url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&query_key=1&WebEnv={}&retstart={}&retmax=500&rettype=json&retmode=json'.format(self.data_ncbi.get()['esearchresult']['webenv'],i)
                ncbi_uids=obtenerJson.apply_async(kwargs={'url': url})
                self.expedientes.append(ncbi_uids)

            #while self.data_ncbi.status == 'PENDING' or self.data_array.status == 'PENDING':
                #time.sleep(1)
            #if self.data_ncbi.get()['esearchresult']['retmax'] == '0' and self.data_array.get()['experiments']['total'] == 0:
                #return render(request,'NoResults.html')
            #else:
            #self.expedientes=self.obtenerExpedientes(self.data_ncbi)

            return render(request,'loader.html')
        else:
            return render(request,'index.html')

    def obtenerExpedientes(self,resultados_busqueda):
        resultados=[]
        while resultados_busqueda.status == 'PENDING':
            time.sleep(1)
        for i in range(len(resultados_busqueda.get()['esearchresult']['idlist'])):
            identificador=resultados_busqueda.get()['esearchresult']['idlist'][i]
            url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id={}&retmode=json'.format(identificador)
            data=obtenerJson.apply_async( kwargs={'url': url})
            resultados.append(data)
        return resultados
    def enviarDatos(self,request):
        informacion = tratamientosDatos(self.expedientes,self.data_array)
        lista=[]
        lista=informacion.unirVectores()
        return  JsonResponse(lista, safe=False)
    def cargarPaginaBusqueda(self,request):
        if self.data_ncbi.get()['esearchresult']['retmax'] == '0' and self.data_array.get()['experiments']['total'] == 0:
            return render(request,'NoResults.html')
        else:
            while self.expedientes[len(self.expedientes)-1].status == 'PENDING' or self.data_array.status == 'PENDING' :
                time.sleep(1)
            informacion = tratamientosDatos(self.expedientes,self.data_array)
            lista=informacion.unirVectores()
            paginator = Paginator(lista, 20) # Show 25 contacts per page
            page = request.GET.get('page')
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
            return render(request,'listarBusqueda.html',{'contacts': contacts})
class tratamientosDatos(models.Model):
    def __init__(self, resultados_ncbi, resultados_array):
        self.datos_ncbi=resultados_ncbi[:]
        self.resultados_array=resultados_array
        self.j=0
    def almacenar_datos_visualizacion_array(self):
        visualizacion_array=[]
        for i in self.resultados_array.get()['experiments']['experiment']:
            if 'experimenttype' in i:
                tipoexperimento=i['experimenttype' ][0]
            else:
                tipoexperimento='Information not available'
            visualizacion_array.append({'id': i['id'],
            'accession': i['accession'],
            'name': i['name'], 'releasedate': i['releasedate'],
             'description': i['description'][0]['text'],'bd': 'arrayexpress',
             'descarga': "https://www.ebi.ac.uk/arrayexpress/experiments/{}/files/".format(i['accession']),
             'especie' : i['organism'][0], 'tipoexperimento' : tipoexperimento,
             'muestras' :'0'})
        return visualizacion_array
    def almacenar_datos_visualizacion_ncbi(self):
        visualizacion_ncbi=[]
        for i in self.datos_ncbi:
            for j in i.get()['result']['uids']:
                identificador=j
                visualizacion_ncbi.append({'id': identificador,
                'accession': i.get()['result'][identificador]['accession'],
                'name':  i.get()['result'][identificador]['title'],
                'releasedate': i.get()['result'][identificador]['pdat'],
                'description':  i.get()['result'][identificador]['summary'],
                'bd': 'ncbi_gds', 'descarga': i.get()['result'][identificador]['ftplink'],
                'especie': i.get()['result'][identificador]['taxon'],
                'tipoexperimento': i.get()['result'][identificador]['gdstype'],
                'muestras': i.get()['result'][identificador]['n_samples']})
        return visualizacion_ncbi

    def unirVectores(self):
        vector_busqueda=[]
        vector_array=[]
        if len(self.datos_ncbi)>0:
            vector_busqueda=self.almacenar_datos_visualizacion_ncbi()
            if self.resultados_array.get()['experiments']['total']>0:
                for i in self.almacenar_datos_visualizacion_array():
                    vector_busqueda.append(i)
        elif self.resultados_array.get()['experiments']['total'] >0:
            vector_busqueda=self.almacenar_datos_visualizacion_array()
        return vector_busqueda



'''
class descargaDeContenido():
    def enlacesFTP(self,request):
        if request.method == 'POST':
            enlace=request.POST['enlace']
            direccion=enlace.split('//',1)
            direccion_cortada=direccion[1].split('/',1)
            ftp = FTP()
            ftp.connect(direccion_cortada[0],21,-999)
            ftp.login()
            ftp.cwd(direccion_cortada[1])

            dirs=ftp.nlst()
            for i in dirs:
                ftp.cwd(i)
                arch=ftp.nlst()
                for j in arch:
                    print("sdfsdfsdf")
                    #ftp.retrbinary('RETR %s' % os.path.basename(j),file_handler)#La recepción
                    print("sdfsdfsdf")
                    #archivo = eg.filesavebox(title="Guardar",
                    #default=j)
                    tam=archivo.count('/')
                    ruta_guardado=""
                    for rut in archivo.split('/',tam):
                        ruta_guardado+='/'
                        ruta_guardado+=rut
                    ftp.retrbinary('RETR '+j, open('~/', 'wb').write)
            ftp.quit()
            return null
'''
#def busqueda_avanzada(palabra_clave, tecnologia_secuenciacion,localizacion, organismo, base_datos):
#	if (base_datos=="ncbi"):



def index(request):
	return render(request, 'index.html')
