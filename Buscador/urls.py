from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^rest/$', views.probando_REST, name='probandoRest'),
   url(r'^busqueda/$', views.buscar, name='buscarDatos'),
  ]
