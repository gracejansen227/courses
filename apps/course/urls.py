from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^destroy/(?P<course_id>\d+)/', views.destroy),
    url(r'^confirm/(?P<course_id>\d+)/', views.confirm),
  ]
