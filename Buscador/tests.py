from django.test import TestCase
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from django.test import Client
from django.test.client import RequestFactory
from celery.result import AsyncResult
import json, requests
from . import views
from Buscador.tasks import obtenerJson
from django.core import serializers
class Busqueda(TestCase):
	def setUp(self):
		self.c = Client()
		self.buscador = views.buscador()
		self.url_ncbi = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=prostata&datetype=edat&retmax=2&usehistory=y&retmode=json'
		self.resultados =[]
		self.url_array = 'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments?assaycount=5&keywords=prostata'
	def test_web_search(self):
		self.assertEqual(self.c.post('/buscador/').status_code,200)
	def test_web_result(self):
		self.assertEqual(self.c.get('/buscador/busqueda/').status_code,200)
	def test_task(self):
		self.data_ncbi=obtenerJson.apply_async(kwargs={'url': self.url_ncbi})
		self.assertIsNotNone(self.data_ncbi)
		self.assertIsInstance(self.data_ncbi,AsyncResult)
	def test_obtenerExpedientes(self):
		self.data_ncbi=obtenerJson.apply_async(kwargs={'url': self.url_ncbi})
		self.assertIsInstance(self.buscador.obtenerExpedientes(self.data_ncbi),list)
		self.resultados = self.buscador.obtenerExpedientes(self.data_ncbi)
		self.assertIsNotNone(self.resultados)
		self.assertIsInstance(self.resultados.pop(),AsyncResult)
	def test_enviarDatos(self):
		self.data_ncbi=obtenerJson.apply_async(kwargs={'url': self.url_ncbi})
		self.buscador.expedientes=self.buscador.obtenerExpedientes(self.data_ncbi)
		self.buscador.data_array=self.data_array = obtenerJson.apply_async(kwargs={'url': self.url_array})
		request=RequestFactory().get('/buscador/', search='prostata')
		self.assertIsNotNone( self.buscador.enviarDatos(request))
		self.assertIsInstance(json.loads(self.buscador.enviarDatos(request).content.decode('utf-8')), list)
	def test_buscador(self):
		self.assertIsInstance(self.buscador, views.buscador)
