from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from customer.models import User, City, SeatClass, Option
from django.core.cache import cache
from main.settings import CURRENCY
import string, random
from .tasks import send_mail_task
from django.db import IntegrityError



@csrf_exempt
def signin(request):
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('password'):
            username = request.POST['username'].lower().strip()
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('cabinet'))
    return render(request, 'signin.html', {})



def signout(request):
    logout(request)
    return redirect(reverse('signin'))



def first_step(request):
    if not request.session.session_key:
        request.session.save()
    key = request.session.session_key
    cities = City.objects.all()
    flight_data = cache.get(key) if cache.get(key) else {}
    if request.method == 'GET':
        return render(request, 'first_step.html', {'data':cities, 'flight_data':flight_data})

    if request.method == 'POST':
        flight_data['source'] = request.POST.get('source')
        flight_data['destination'] = request.POST.get('destination')
        flight_data['datetime'] = request.POST.get('datetime')
        flight_data['passengers'] = request.POST.get('passengers')
        cache.set(key, flight_data)
        return redirect(reverse('second_step'))



def second_step(request):
    key = request.session.session_key
    flight_data = cache.get(key)
    flight_data['currency'] = CURRENCY
    seat_class = SeatClass.objects.all()
    option = Option.objects.all()
    if request.method == 'GET':
        data = {}
        for i in seat_class:
            data[i.name] = i.price
        for i in option:
            data[i.name] = i.price
        return render(request, 'second_step.html', {'data':data, 'flight_data':flight_data})

    if request.method == 'POST':
        if 'lunch' in request.POST:
            flight_data['lunch'] = True
        if 'luggage' in request.POST:
            flight_data['luggage'] = True
        flight_data['seat_class'] = request.POST['seat_class']
        cache.set(key, flight_data)
        return redirect(reverse('third_step'))



def third_step(request):
    key = request.session.session_key
    flight_data = cache.get(key)
    if request.method == 'GET':
        return render(request, 'third_step.html', {'flight_data':flight_data})
    if request.method == 'POST':
        flight_data['first_name'] = request.POST['first_name']
        flight_data['last_name'] = request.POST['last_name']
        flight_data['email'] = request.POST['email']
        flight_data['username'] = request.POST['email']
        flight_data['password'] = get_random_password()
        try:
            user = User.objects.create_user(username=flight_data['username'], email=flight_data['email'],
                                       first_name=flight_data['first_name'], last_name=flight_data['last_name'],
                                       is_active=True, password=flight_data['password'])
            flight_data['exists'] = False
            send_mail_task.delay(flight_data)
            cache.set(key, flight_data)
            return render(request, 'user.html', flight_data)
        except IntegrityError:
            flight_data['exists'] = True
            send_mail_task.delay(flight_data)
            cache.set(key, flight_data)
            return render(request, 'user.html', flight_data)



def get_random_password():
    str = string.ascii_letters + string.digits
    return ''.join([random.choice(str) for i in range(8)])



@login_required(login_url='/signin/')
def cabinet(request):
    return render(request, 'cabinet.html', {})



@login_required(login_url='/signin/')
def checkin(request):
    data = {}
    key = request.session.session_key
    flight_data = cache.get(key) if cache.get(key) else {}
    if request.method == 'GET':
        data['cities'] = City.objects.all()
        seat_class = SeatClass.objects.all()
        option = Option.objects.all()
        for i in seat_class:
            data[i.name] = i.price
        for i in option:
            data[i.name] = i.price
        return render(request, 'checkin.html', {'data':data, 'flight_data':flight_data})

    if request.method == 'POST':
        flight_data['source'] = request.POST.get('source')
        flight_data['destination'] = request.POST.get('destination')
        flight_data['datetime'] = request.POST.get('datetime')
        flight_data['passengers'] = request.POST.get('passengers')
        flight_data['exists'] = True
        flight_data['currency'] = CURRENCY

        if 'lunch' in request.POST:
            flight_data['lunch'] = True
        if 'luggage' in request.POST:
            flight_data['luggage'] = True
        flight_data['seat_class'] = request.POST['seat_class']
        cache.set(key, flight_data)
#        return redirect(reverse('cabinet'))
        print(flight_data)
        return render(request, 'ticket.html', {'flight_data':flight_data})
