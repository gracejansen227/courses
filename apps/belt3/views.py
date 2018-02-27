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

    return render(request, 'belt3/index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        birthday = request.POST['birthday']

        request.session['email'] = request.POST['email']

        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        User.objects.create(first_name= first_name, alias=alias, email=email, birthday=birthday, password=hash1)
        request.session['first_name'] = first_name
        request.session['alias'] = alias

        return redirect('/friends')


def login(request):

    request.session['email'] = request.POST['email']

    loginpw = request.POST['loginpw']

    if User.objects.filter(email= request.POST['email']):
        check_pw = User.objects.get(email=request.POST['email']).password


        if bcrypt.checkpw(loginpw.encode(), check_pw.encode()) == False:
            messages.error(request, "Passwords don't match fool!")
            print "doesn't equal encripted"
            return redirect('/')
        else:
            #loginusername = request.POST['user_name']

            check_pw_user = User.objects.get(email=request.POST['email'])
            first_name = check_pw_user.first_name
            print first_name

            request.session['first_name'] = first_name

        return redirect('/friends')
    else:
        messages.error(request, "This email has not been registered!")
        return redirect('/')

def friends(request):


    success_user = User.objects.get(email=request.session['email'])

    success_user_id = success_user.id

    notfriends = []
    my_friends = []
    all_users = User.objects.all()
    # if all_users.id = success_user.id:
    #     all_users

    my_friends = success_user.friends.all()

    for user in all_users:
        if user.id != success_user_id:
            if user not in my_friends:
                notfriends.append(user)

    context = {
     "my_friends" : my_friends,
     "notfriends" : notfriends,
     "all_users" : all_users,
        }

    return render(request, 'belt3/friends.html', context)

def show(request, friend_id):
    this_user = User.objects.get(id=friend_id)
    context = {
        "friend_id" : friend_id,
        "first_name" : this_user.first_name,
        "alias" : this_user.alias,
        "email" : this_user.email,
    }
    return render(request, 'belt3/show.html', context)

def delete(request, id):

    delete_friend = User.objects.get(id=id)

    success_user = User.objects.get(email=request.session['email'])

    success_user.friends.remove(delete_friend)

    return redirect('/friends')

def add(request, user_id):
    add_friend = User.objects.get(id=user_id)

    success_user = User.objects.get(email=request.session['email'])

    success_user.friends.add(add_friend)

    return redirect('/friends')

def logout(request):
    request.session.clear()
    return redirect('/')
