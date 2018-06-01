from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# This is all the validation
class UserManager(models.Manager):
    def register(self, postData):
        errors = {}
        if len(postData['full_name']) < 2:
            errors['full_name'] ='Please input full name.'
        if len(postData['username']) <  2:
            errors['uername']= 'Please input a username.' 
        if len(postData['password']) < 8:
           errors['password'] ='Password must be at least 8 characters.'
        if postData['password'] != postData['passwordconf']:
            errors['passwordconf'] ='Passwords must match.'     
        if len(errors) > 0:
            status = {
                'errors': errors,
                'valid': False
            }
            return status
        else:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(
                full_name = postData['full_name'],
                username = postData['username'], 
                password = hashed_password)
            status = {
                'user': user,
                'valid': True
            }
        return status


    def login(self, postData):
        errors = {}
        user = User.objects.filter(username = postData['username'])
        status = {
            'verified' : False,
            'errors' : errors,
        }
        errors['username'] = 'Please enter a valid username and password.'
        print(errors['username'])
        if len(user) > 0 and bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            status['user'] = user[0]
            status['verified'] = True
        return status


class User(models.Model):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {}>".format(self.full_name, self.username)




class TripManager(models.Manager):
    def createTrip(self, postData, user_id):
        now = datetime.now()
        errors = {}
        status = {
            'valid' : True
        }
        if len(postData['destination']) < 2:
            errors['destinaion'] ='Please provide a destination.'
        if len(postData['description']) <  2:
            errors['description']= 'Please provide a description.' 
        if len(postData['trip_start']) < 2:
           errors['trip_start'] ='Please provide departure date.'
        if len(postData['trip_end']) < 2:
           errors['trip_end'] ='Please provide return date.'
        
        # else: 
        #     trip_start = datetime.strptime(postData['trip_start'], %Y-%m-%d)

        if len(errors) > 0:
            status = {
                'errors': errors,
                'valid': False
            }
            return status
        else:
            user = User.objects.get(id=user_id)
            trip = Trip.objects.create(
                destination = postData['destination'],
                description = postData['description'], 
                trip_start = postData['trip_start'],
                trip_end = postData['trip_end'],
                creater = user,
            )
            trip.attendees.add(user)
            trip.save()
        return status
    
    def join(self, trip_id, user_id):
        user = User.objects.get(id=user_id)
        trip = Trip.objects.get(id=trip_id)
        trip.attendees.add(user)
        trip.save()
    
    def remove(self, trip_id, user_id):
        user = User.objects.get(id=user_id)
        trip = Trip.objects.get(id=trip_id)
        trip.attendees.remove(user)
        trip.save()

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    trip_start = models.DateField()
    trip_end = models.DateField()
    creater = models.ForeignKey(User, related_name="trip_creater", null=True)
    attendees = models.ManyToManyField(User, related_name="attending_trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()
    def __repr__(self):
        return "<Trip object: {} {} {} {}>".format(self.destination, self.description, self.trip_start, self.trip_end)