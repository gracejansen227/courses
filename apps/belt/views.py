# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

import datetime
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, HttpResponse, redirect
from models import *
import bcrypt


def index(request):
    registered = ''
    registered == False
    return render(request, 'belt/index.html')

def register(request, methods="POST"):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        birthday = request.POST['birthday']

        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        User.objects.create(first_name= first_name, last_name=last_name, email=email, password=hash1, birthday=birthday)
        request.session['email'] = email

        return redirect('/appointments')


def login(request, methods="POST"):

    loginpw = request.POST['loginpw']
    loginemail = request.POST['email']
    print loginemail, "does this print the right email"
    if User.objects.filter(email= loginemail):
        check_pw = User.objects.get(email=loginemail).password
        print check_pw

        if bcrypt.checkpw(loginpw.encode(), check_pw.encode()) == False:
            messages.error(request, "Passwords don't match fool!")
            print "doesn't equal encripted"
            return redirect('/')
        else:
            loginemail = request.POST['email']
            print request.POST['email']
            check_pw_user = User.objects.get(email=loginemail)
            first_name = check_pw_user.first_name
            print first_name
            request.session['email'] = loginemail
            request.session['first_name'] = first_name
        print "checked password worked"
        return redirect('/appointments')
    else:
        messages.error(request, "This email has not been registered!")
        return redirect('/')

def appointments(request):
    now = datetime.datetime.now()
    request.session['today'] = str(now)
    print str(now)
    print timezone.now()
    print request.session['email']
    success_user = User.objects.get(email=request.session['email'])
    print success_user.first_name
    request.session['name'] = success_user.first_name
    users_appointments = User.objects.get(email=request.session['email'])

    users_appointments = users_appointments.all_users_appointments.all()
    print users_appointments
    today_appointments = users_appointments.filter(date=(now))
    #today_appointments = Appointment.objects.filter(date=(now))
    print today_appointments

    success_appointments = users_appointments.exclude(date=(now))
    #success_appointments = Appointment.objects.exclude(date=(now))
    print success_appointments

    context = {
        "success_appointments" : success_appointments,
        "today_appointments" : today_appointments
            }

    return render(request, 'belt/appointments.html', context)

def showedit(request, id):

    return render(request,'belt/edit.html', {'appointment_id' : id})

def edit(request, appointment_id, methods="POST"):
    errors = Appointment.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/appointments')
    else:
        edit_appointment = Appointment.objects.get(id=appointment_id)
        new_task = request.POST['task']
        new_status = request.POST['status']
        new_date = request.POST['date']
        new_time = request.POST['time']


        edit_appointment.task = new_task
        edit_appointment.status = new_status
        edit_appointment.date = new_date
        edit_appointment.time = new_time
        edit_appointment.save()

        context = {
        "appointment_id" : appointment_id,
        "task" : edit_appointment.task,
        "status" : edit_appointment.status,
        "date" : edit_appointment.date,
        "time" : edit_appointment.time,
        }
        return redirect('/belt/appointments', context)

def delete(request, id):
    delete_appointment = Appointment.objects.get(id=id)
    delete_appointment.delete()

    return redirect('/appointments')

def add(request, methods="POST"):
    errors = Appointment.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/appointments')
    else:
        user_email = request.session['email']
        task = request.POST['task']
        date = request.POST['date']
        status = request.POST['status']
        time = request.POST['time']

        appointment_user_id = User.objects.get(email=user_email).id
        print appointment_user_id
        print time

        Appointment.objects.create(task = task, date = date, time =time, status= status, appointment_user_id = appointment_user_id)

        user = User.objects.get(email=user_email)
        #all_appointments = user.all_users_appointments.all()
        all_appointments = Appointment.objects.all()

        return redirect('/appointments',{
            "all_appointments" : Appointment.objects.all()
            })
