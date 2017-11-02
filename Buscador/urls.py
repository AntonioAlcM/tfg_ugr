from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^devolverJSON/$', views.devuelve_estado, name='verEstado'),
  ]
