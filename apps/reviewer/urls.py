from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^books$', views.books),
    url(r'^showadd$', views.showadd),
    url(r'^reviewer/add$', views.add),
  ]
