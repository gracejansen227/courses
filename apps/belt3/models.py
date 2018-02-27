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
        if len(postData['first_name']) <3:
            errors["first_name"] = "First name must be longer than 2 characters!"
        if not postData['first_name'].isalpha:
            errors["first_name"] = "First name can only contain letters!"

        if len(postData['alias']) < 0:
            errors["alias"] = "Alias cannot be blank!"
        if len(postData['alias']) <3:
            errors["alias"] = "Alias must be longer than 2 characters!"


        alias_exists = User.objects.filter(alias=postData['alias'])
        if len(alias_exists) !=0:
            errors["alias"] = "Alias already exists!"

        if len(postData['password']) < 1:
            errors['password']= "Password cannot be empty!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be longer than 8 characters!"


        if len(postData['confirmpw']) < 1:
            errors['confirmpw'] = "Please confirm password!"

        if postData['confirmpw'] != postData['password']:
            errors['confirmpw'] = "Passwords do not match!"
        if len(postData['email']) < 1:
            errors['email']= "Email cannot be empty!"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        email_exists = User.objects.filter(email=postData['email'])
        if len(email_exists) !=0:
            errors["email"] = "Email already exists!"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    friends = models.ManyToManyField('self')

    objects = UserManager()
