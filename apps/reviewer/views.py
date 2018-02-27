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
    registered = ''
    registered == False
    return render(request, 'reviewer/index.html')

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

        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        User.objects.create(first_name= first_name, last_name=last_name, email=email, password=hash1)
        request.session['email'] = email

        request.session['first_name'] = first_name

        return redirect('/books')


def login(request, methods="POST"):

    request.session['email'] = request.POST['email']

    loginpw = request.POST['loginpw']


    if User.objects.filter(email= request.POST['email']):
        check_pw = User.objects.get(email=request.POST['email']).password
        print check_pw

        if bcrypt.checkpw(loginpw.encode(), check_pw.encode()) == False:
            messages.error(request, "Passwords don't match fool!")
            print "doesn't equal encripted"
            return redirect('/')
        else:

            print request.POST['email']
            check_pw_user = User.objects.get(email=request.POST['email'])
            first_name = check_pw_user.first_name
            request.session['first_name'] = first_name
        print "checked password worked"
        return redirect('/books')
    else:
        messages.error(request, "This email has not been registered!")
        return redirect('/')

def books(request):
    all_reviews = Review.objects.all().order_by('-created_at')
    first_reviews = []
    rest_reviews = []
    i = 0
    for reviews in all_reviews:
        if i < 3:
            first_reviews.append(reviews)
            i+=1
        else:
            rest_reviews.append(reviews)


    context = {
    "first_reviews": first_reviews,
    "rest_reviews" : all_reviews,
    }

    return render(request, 'reviewer/books.html', context)

def showadd(request):
    return render(request, 'reviewer/add.html')

def add(request):
    user_email = request.session['email']
    user_id = User.objects.get(email=user_email).id
    reviewer = User.objects.get(id=user_id).first_name

    title = request.POST['title']
    author = request.POST['author']
    review = request.POST['review']
    rating = request.POST['rating']

    this_book = Book.objects.create(title=title, author=author)
    context = {
        "title" :title,
        "reviewer": reviewer
    }
    # book_id = this_book.id
    #
    # book_id.

    # this_book_review.book_reviews.add(reviewer=user_id)
    Review.objects.create(review=review, rating=rating, reviewer_id=user_id)


    return redirect('/books', context)
