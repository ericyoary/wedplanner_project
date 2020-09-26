from django.db import models
import re
import bcrypt
import datetime
from django.utils.dateparse import parse_date
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0:
            errors['first_name'] = 'First name is required'
        elif len(postData['first_name']) < 2 or postData['first_name'].isalpha() != True:
            errors['first_name'] = 'First name must be at least 2 characters long, letters only'
        if len(postData['last_name']) == 0:
            errors['last_name'] = 'Last name is required'
        elif len(postData['last_name']) < 2 or postData['last_name'].isalpha() != True:
            errors['last_name'] = 'Last name must be at least 2 characters long, letters only'     
        if len(postData['email']) == 0:
            errors['email'] = 'Email is required'
        elif not email_regex.match(postData['email']):
            errors['email'] = 'Invalid email format'
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) != 0:
            errors['email'] = 'Email already in use'
        if len(postData['password']) == 0:
            errors['password'] = 'Password is required'
        elif len(postData['password']) < 5:
            errors['password'] = 'Password must be at least 5 characters long'
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = 'Password and confirm password inputs must match'
        return errors
    
    def log_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) ==0:
            errors ['email'] = "Email not registered" 
        else:
            logged_user = existing_user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                pass
            else:
                errors['password'] = "Password not correct"
        if len(postData['password']) == 0:
                errors['password'] = 'Password is required'
        elif len(postData['password']) < 5:
            errors['password'] = 'Password must be at least 5 characters long' 
        return errors
        # errors = {}
        # if len(postData['email']) == 0:
        #     errors['email'] = 'Email is required'
        # elif not email_regex.match(postData['email']):
        #     errors['email'] = 'Invalid email format'    
        # existing_user = User.objects.filter(email=postData['email'])
        # if len(existing_user) != 1:
        #     errors['email'] = 'User not found'      
        # if len(postData['password']) == 0:
        #     errors['password'] = 'Password is required'
        # elif len(postData['password']) < 5:
        #     errors['password'] = 'Password must be at least 5 characters long'    
        # elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].
        # password.encode()) != True:
        #     errors['email'] = 'Email and password do not match'
        # return errors
    
# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    #created_at = models.DateTimeField
    #updated_at = models.DateTimeField
    
    objects = UserManager()
    
class WeddingManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['wedder_one']) == 0:
            errors['wedder_one'] = 'Wedder One field required'
        if len(postData["wedder_two"]) == 0:
            errors["wedder_two"] = 'Wedder Two field required'
        if len(postData['wedding_date']) == 0:
            errors['wedding_date'] = 'Weddding Date field required'
        elif parse_date(postData['wedding_date']) < datetime.date.today():
            errors['wedding_date'] = 'Date cannot be in the past'
        if len(postData['address']) == 0:
            errors['address'] = 'Address field required'

        return errors
    
class Wedding(models.Model):
    wedder_one = models.CharField(max_length=60)
    wedder_two = models.CharField(max_length=60)
    wedding_date = models.DateField()
    address = models.CharField(max_length=255)
    planner = models.ForeignKey(User, related_name='weddings_planned', on_delete=models.CASCADE)
    guests = models.ManyToManyField(User, related_name='weddings_attended')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = WeddingManager()