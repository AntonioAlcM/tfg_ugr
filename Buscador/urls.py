from django.conf.urls import url
from . import views
from .views import buscador
busca=buscador()
urlpatterns = [
  url(r'^$', views.index, name='index'),
   url(r'^busqueda/$', busca.buscar, name='buscarDatos'),
    url(r'^recibirDatos/$', busca.enviarDatos, name='recibirDatos'),
    #url(r'^descargaFTP/$', views.descargaDeContenido().enlacesFTP, name='enlacesFTP'),
    url(r'^cargarPaginaBusqueda/$', busca.cargarPaginaBusqueda, name='cargarPaginaBusqueda'),
  ]
