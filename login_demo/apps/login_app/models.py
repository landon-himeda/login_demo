from __future__ import unicode_literals
from django.db import models
import bcrypt



# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # Check if the password is 8 characters long
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        return errors

    def login_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 5:
            errors["name"] = "Blog name should be at least 5 characters"
        if len(postData['desc']) < 10:
            errors["desc"] = "Blog description should be at least 10 characters"
        return errors


class User(models.Model):
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()    # add this line!