# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.db import models
import bcrypt
import re
from django.utils import timezone
import datetime

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 0:
            errors["first_name"] = "First name cannot be blank!"
        if len(postData['first_name']) <2:
            errors["first_name"] = "First name must be longer than 2 characters!"
        if not postData['first_name'].isalpha:
            errors["first_name"] = "First name can only contain letters!"

        if len(postData['last_name']) < 0:
            errors["last_name"] = "Last name cannot be blank!"
        if len(postData['last_name']) <2:
            errors["last_name"] = "Last name must be longer than 2 characters!"
        if not postData['last_name'].isalpha():
                errors["last_name"] = "Last name can only contain letters!"

        if len(postData['email']) < 1:
            errors['email']= "Email cannot be empty!"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        email_exists = User.objects.filter(email=postData['email'])
        if len(email_exists) !=0:
            errors["email"] = "Email already exists!"

        if len(postData['password']) < 1:
            errors['password']= "Password cannot be empty!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be longer than 8 characters!"


        if len(postData['confirmpw']) < 1:
            errors['confirmpw'] = "Please confirm password!"

        if postData['confirmpw'] != postData['password']:
            errors['confirmpw'] = "Passwords do not match!"
        return errors

class AppointmentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        now = datetime.datetime.now()
        if len(postData['task']) < 0:
            errors["task"] = "Task cannot be blank!"
        if len(postData['date']) < 0:
            errors["date"] = "Date cannot be blank!"
        # inputed_date = datetime.strptime(postData["date"], '%Y-%m-%d')
        if postData['date'] < str(now):
            errors['date'] = "Cannot make appointment in the past!!"

        print timezone.now()
        # if inputed_date < datetime.today().date():
        #     errors["date"] = "Date cannot be in the past!"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)

    objects = UserManager()

class Appointment(models.Model):
    task = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=15)
    appointment_user = models.ForeignKey(User, related_name = "all_users_appointments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)

    objects = AppointmentManager()
