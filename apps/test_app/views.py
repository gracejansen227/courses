# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from models import *
import bcrypt

def index(request):
    return render(request, 'test_app/index.html')

def signinpage(request):
    return render(request, 'test_app/signin.html')

def signin(request, methods="POST"):

    signinpw = request.POST['loginpw']
    signinemail = request.POST['email']
    print signinemail, "does this print the right email"
    if User.objects.filter(email= signinemail):
        check_pw = User.objects.get(email=signinemail).password
        print check_pw

        if bcrypt.checkpw(signinpw.encode(), check_pw.encode()) == False:
            messages.error(request, "Passwords don't match fool!")
            print "doesn't equal encripted"
            return redirect('/test_app')
        else:
            signinemail = request.POST['email']
            print request.POST['email']
            check_pw_user = User.objects.get(email=signinemail)

            request.session['email'] = signinemail
        print "checked password worked"
        return redirect('/test_app/show')
    else:
        messages.error(request, "This email has not been registered!")
        return redirect('/test_app')


def show(request):
    #show friggen prfile page of userinformation
    #AHHHH
    render
def
#shows the manage- admin dashboard
def dashboard(request):
    return render(request, 'test_app/manage.html')

def show(request):






def register(request, methods="POST"):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/login_reg')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        User.objects.create(first_name= first_name, last_name=last_name, email=email, password=hash1)
        request.session['email'] = email

        return redirect('/login_reg/success')


def login(request, methods="POST"):
    #if email exists in database already
    #else redirect and give error message (email not registered!)
    #if registered == True:
    loginpw = request.POST['loginpw']
    loginemail = request.POST['email']
    print loginemail, "does this print the right email"
    if User.objects.filter(email= loginemail):
        check_pw = User.objects.get(email=loginemail).password
        print check_pw

        if bcrypt.checkpw(loginpw.encode(), check_pw.encode()) == False:
            messages.error(request, "Passwords don't match fool!")
            print "doesn't equal encripted"
            return redirect('/login_reg')
        else:
            loginemail = request.POST['email']
            print request.POST['email']
            check_pw_user = User.objects.get(email=loginemail)

            request.session['email'] = loginemail
        print "checked password worked"
        return redirect('/login_reg/success')
    else:
        messages.error(request, "This email has not been registered!")
        return redirect('/login_reg')

def success(request):
    print request.session['email']
    success_user = User.objects.get(email=request.session['email'])

    context = {
        "first_name" : success_user.first_name,
        "last_name" : success_user.last_name,
        }

    return render(request, 'login_reg/success.html', context)
