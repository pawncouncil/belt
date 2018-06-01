from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *


def index(request):
    return render(request, 'beltApp/index.html')

def register(request):
    status = User.objects.register(request.POST)
    if status['valid']==False:
        for key, value in status['errors'].items():
            messages.error(request, value)
            return redirect('/')
    else:
        request.session['user_id'] = status['user'].id 
        return redirect('/main')

def login(request):
    status = User.objects.login(request.POST)
    if status['verified'] == False:
        for error, value in status['errors'].items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session['user_id'] = status['user'].id 
        return redirect('/main')

def logout(request):
    if 'user_id' not in request.session:
        return redirect('/')
    request.session.clear()
    return redirect('/')




def main(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'user' : user,
        'schedule' : Trip.objects.filter(attendees=request.session['user_id']),
        'others_trips' : Trip.objects.exclude(attendees=request.session['user_id'])
    }
    return render(request, 'beltApp/main.html', context)

def add(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'beltApp/add.html')

def createTrip(request):
    if 'user_id' not in request.session:
        return redirect('/')
    status = Trip.objects.createTrip(request.POST, request.session['user_id'])
    if status['valid']==False:
        for key, value in status['errors'].items():
            messages.error(request, value)
            return redirect('/add')
    else:
        return redirect('/main')

def join(request, trip_id):
    if 'user_id' not in request.session:
        return redirect('/')
    Trip.objects.join(user_id=request.session['user_id'], trip_id=trip_id)
    return redirect('/main')


def remove(request, trip_id):
    if 'user_id' not in request.session:
        return redirect('/')
    Trip.objects.remove(user_id=request.session['user_id'], trip_id=trip_id)
    return redirect('/main')


def destination(request, trip_id):
    if 'user_id' not in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    context = {
        'destination' : trip,
        'attendees' : trip.attendees.exclude(id = trip.creater.id)
    }
    return render(request, 'beltApp/destination.html', context)

def delete(request, trip_id):
    if 'user_id' not in request.session:
        return redirect('/')
    t = Trip.objects.get(id = trip_id)
    t.delete()
    return redirect('/main')