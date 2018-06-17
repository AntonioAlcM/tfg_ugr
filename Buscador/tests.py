from django.test import TestCase
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from django.test import Client
from django.test.client import RequestFactory
from celery.result import AsyncResult
import json, requests
from . import views
from Buscador.tasks import obtenerJson
from django.core import serializers
class TestBusqueda(TestCase):
	def setUp(self):
		self.c = Client()
		self.buscador = views.Buscador()
		self.url_ncbi = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=mela&datetype=edat&retmax=2&usehistory=y&retmode=json'
		self.resultados =[]
		self.url_array = 'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments?keywords=mela'
		self.data_ncbi=obtenerJson.apply_async(kwargs={'url': self.url_ncbi})
		self.expedientes=self.buscador.obtenerExpedientes(self.data_ncbi)
		self.data_array = obtenerJson.apply_async(kwargs={'url': self.url_array})
		self.tratamientoDatos=views.TratamientosDatos(self.expedientes, self.data_array)
	def test_web_search(self):
		self.assertEqual(self.c.post('/buscador/').status_code,200)
	def test_web_result(self):
		self.assertEqual(self.c.get('/buscador/busqueda/').status_code,200)
	def test_task(self):
		self.assertIsNotNone(self.data_ncbi)
		self.assertIsInstance(self.data_ncbi,AsyncResult)
	def test_obtenerExpedientes(self):
		self.assertIsInstance(self.buscador.obtenerExpedientes(self.data_ncbi),list)
		self.resultados = self.buscador.obtenerExpedientes(self.data_ncbi)
		self.assertIsNotNone(self.resultados)
		self.assertIsInstance(self.resultados.pop(),AsyncResult)
	def test_buscador(self):
		self.assertIsInstance(self.buscador, views.Buscador)
	def test_cargarPaginaBusqueda(self):
		resultado= json.dumps({'ncbi':str(self.data_ncbi),'array':str(self.data_array),'busqueda':"mela"})
		request=RequestFactory().post('/buscador/results/', {'myInput':resultado})
		self.assertIsNotNone( views.cargarPaginaBusqueda(request))
		self.assertEqual(views.cargarPaginaBusqueda(request).status_code,200)
	def test_tratamientoDatos(self):
		self.assertIsInstance(self.tratamientoDatos, views.TratamientosDatos)
	def test_almacenar_datos_visualizacion_ncbi(self):
		self.assertIsNotNone( self.tratamientoDatos.almacenar_datos_visualizacion_ncbi())
		self.assertIsInstance(self.tratamientoDatos.almacenar_datos_visualizacion_ncbi(), list)
	def test_almacenar_datos_visualizacion_array(self):
		self.assertIsNotNone( self.tratamientoDatos.almacenar_datos_visualizacion_array())
		self.assertIsInstance(self.tratamientoDatos.almacenar_datos_visualizacion_array(), list)
	def test_unir_vectores(self):
		self.tratamientoDatos.almacenar_datos_visualizacion_ncbi()
		self.tratamientoDatos.almacenar_datos_visualizacion_array()
		self.assertIsNotNone( self.tratamientoDatos.unirVectores())
		self.assertIsInstance(self.tratamientoDatos.unirVectores(), list)
	def test_inicializarBuscador(self):
		request=RequestFactory().post('/buscador/', {'search':'prostata'})
		self.assertIsNotNone( views.inicializarBuscador(request))
		self.assertEqual(views.inicializarBuscador(request).status_code,200)
	def test_sendFile(self):
		resultado= json.dumps({"accession":self.tratamientoDatos.almacenar_datos_visualizacion_array()[0]['accession'], "file": self.tratamientoDatos.almacenar_datos_visualizacion_array()[0] })
		request=RequestFactory().post('/buscador/expedients/', {'myInput':resultado})
		self.assertIsNotNone( views.sendFile(request))
		self.assertEqual(views.sendFile(request).status_code,200)
