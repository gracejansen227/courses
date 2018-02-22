from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^register$', views.register),
    url(r'^signinpage$', views.signinpage),
    url(r'^(?P<user_id>\d+)/edit$', views.edit),
    url(r'^(?P<user_id>\d+)/delete$', views.delete),
    url(r'^(?P<user_id>\d+)/show$', views.show),
    url(r'^(?P<user_id>\d+)/showedit$', views.showedit),
    url(r'^new$', views.new),
    url(r'^create$', views.create),
  ]
