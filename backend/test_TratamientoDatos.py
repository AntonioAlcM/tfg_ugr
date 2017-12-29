# -*- coding: utf-8 -*-
import unittest
from tratamientoDatos import tratamientosDatos
from Buscador import tasks
import json, time

class TestTratamientoDatos(unittest.TestCase):
	def setUp(self):
		self.url_ncbi = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=prostata&datetype=edat&retmax=2&usehistory=y&retmode=json'
		self.url_array = 'https://www.ebi.ac.uk/arrayexpress/json/v3/experiments?assaycount=1&keywords=prostata'
		self.data_ncbi=tasks.obtenerJson.apply_async(kwargs={'url': self.url_ncbi})
		self.expedientes=self.obtenerExpedientes(self.data_ncbi)
		self.data_array=tasks.obtenerJson.apply_async(kwargs={'url': self.url_array})
		self.tratamiento=tratamientosDatos(self.expedientes,str(self.data_array))
	def test_almacenar_datos_visualizacion_array(self):
		self.assertIsNotNone(self.tratamiento.almacenar_datos_visualizacion_array())
		self.assertIsInstance(self.tratamiento.almacenar_datos_visualizacion_array(),list)
	def test_almacenar_datos_visualizacion_ncbi(self):
		self.assertIsNotNone(self.tratamiento.almacenar_datos_visualizacion_ncbi())
		self.assertIsInstance(self.tratamiento.almacenar_datos_visualizacion_ncbi(),list)
	def test_unirVectores(self):
		self.assertIsNotNone(self.tratamiento.unirVectores())
		self.assertIsInstance(self.tratamiento.unirVectores(),list)
	def obtenerExpedientes(self,resultados_busqueda):
		resultados=[]
		while resultados_busqueda.status == 'PENDING':
			time.sleep(2)
		for i in range(len(resultados_busqueda.get()['esearchresult']['idlist'])):
			identificador=resultados_busqueda.get()['esearchresult']['idlist'][i]
			url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id={}&retmode=json'.format(identificador)
			resultados.append(str(tasks.obtenerJson.apply_async( kwargs={'url': url})))
		return resultados
if __name__ == '__main__':
	unittest.main()
