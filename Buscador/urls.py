from django.conf.urls import url
from . import views
from .views import buscador
busca=buscador()
urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^rest/$', views.probando_REST, name='probandoRest'),
   url(r'^busqueda/$', busca.buscar, name='buscarDatos'),
    url(r'^recibirDatos/$', busca.enviarDatos, name='recibirDatos'),
    url(r'^rest/$', views.probando_REST, name='probandoRest'),
  ]
