from django.test import TestCase
from django.shortcuts import HttpResponse
from django.test import Client
import json
from . import views

class JSONTest(TestCase):
	def setUp(self):
		self.c = Client()
	def test_pagina_recibida(self):
		ruta=self.c.get ('/status/')
		self.assertEqual(ruta.status_code,200)
	def test_json_status_ok(self):
		ruta=json.loads(self.c.get('/status/').content.decode('utf-8'))
		self.assertEqual(ruta["status"],"OK")


class RESTTest(TestCase):
	def setUp(self):
		self.c = Client()
	def test_pagina_recibida_ejemplo(self):
		ruta=self.c.get ('/buscador/rest/')
		self.assertEqual(ruta.status_code,200)
	def test_return_search(self):
		ruta=json.loads(self.c.post('/buscador/rest/').content.decode('utf-8'))
		self.assertEqual(ruta['status'],"OK")
	def test_return_status(self):
		ruta=json.loads(self.c.get ('/buscador/rest/').content.decode('utf-8'))
		self.assertGreater(len(ruta.items()), 0)

class Busqueda(TestCase):
	def setUp(self):
		self.c = Client()
	def test_return_search(self):
		ruta=self.c.post ('/buscador/',{'search': 'cancer'})
		#print (views.objects.get().search)
		self.assertIsNotNone(ruta)
