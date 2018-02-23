from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^appointments$', views.appointments),
    url(r'^(?P<id>\d+)/showedit$', views.showedit),
    url(r'^(?P<id>\d+)/edit$', views.edit),
    url(r'^(?P<id>\d+)/delete$', views.delete),
    url(r'^add$', views.add),

  ]
