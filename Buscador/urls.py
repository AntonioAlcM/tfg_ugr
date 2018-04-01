from django.conf.urls import url
from . import views

from .views import inicializarBuscador,inicializarBuscadorGSE
urlpatterns = [
url(r'^$', views.index, name='index'),
  url(r'^busqueda/$', inicializarBuscador, name='buscarDatos'),
   url(r'^busquedaGSE/$', inicializarBuscadorGSE, name='buscarDatosGSE'),
   #url(r'^descargaFTP/$', views.descargaDeContenido, name='descargaFTP'),
   url(r'^results/$', views.cargarPaginaBusqueda, name='cargarPaginaBusqueda'),
   url(r'^expedient/$', views.sendFile, name='seeExpedient'),
  ]
