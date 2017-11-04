from django.test import TestCase
from django.shortcuts import HttpResponse
from django.test import Client
from . import views

class JSONTest(TestCase):
	def setUp(self):
		self.c = Client()
	def test_pagina_recibida(self):
		ruta=self.c.get ('/')
		self.assertEqual(ruta.status_code,200)
	def test_json_status_ok(self):
		ruta=self.c.get ('/')
		self.assertEqual(ruta.json()['status'],"OK")
	def test_pagina_recibida_ejemplo(self):
		ruta=self.c.get ('/buscador/ejemplo/')
		self.assertEqual(ruta.status_code,200)
	def test_json_ejemplo(self):
		ruta=self.c.get ('/buscador/ejemplo/')
		self.assertEqual(ruta.json()['status'],"OK")

class RESTTest(TestCase):
	def setUp(self):
		self.c = Client()
	def test_pagina_recibida_ejemplo(self):
		ruta=self.c.get ('/buscador/rest/')
		self.assertEqual(ruta.status_code,200)
	def test_return_search(self):
		ruta=self.c.post ('/buscador/rest/')
		self.assertEqual(ruta.json()['status'],"OK")
	def test_return_status(self):
		ruta=self.c.get ('/buscador/rest/')
		print(len(ruta.json().items()))
		self.assertGreater(len(ruta.json().items()), 0)