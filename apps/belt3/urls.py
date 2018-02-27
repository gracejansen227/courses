from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
     url(r'^login$', views.login),
     url(r'^register$', views.register),
    url(r'^friends$', views.friends),
    url(r'^(?P<user_id>\d+)/add$', views.add),
    url(r'^(?P<id>\d+)/delete$', views.delete),
    url(r'^(?P<friend_id>\d+)/show$', views.show),
    url(r'^logout$', views.logout),

  ]
