# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from models import *

def index(request):
    print "is this going to index"
    return HttpResponse("ghello")
    #return render(request, 'course/index.html', {'courses': Course.objects.all()})

def create(request, methods="POST"):
    errors = Course.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/course')
    else:
        name = request.POST['name']
        desc = request.POST['desc']

        Course.objects.create(name= name, desc= desc)

        return redirect('/course')

def destroy(request, course_id):
    course_destroy = Course.objects.get(id=course_id)
    context = {
    "course_id" : course_id,
    "name" : course_destroy.name,
    "desc" : course_destroy.desc
    }
    return render(request, 'course/destroy.html', context)

def confirm(request, course_id):
    delete_course = Course.objects.get(id=course_id)
    delete_course.delete()
    return redirect('/course')

def deny(request):
    return redirect('/course')
