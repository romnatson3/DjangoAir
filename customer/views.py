from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, City, Option, SeatClass, Flight, Ticket, Airplane, Gate
from django.core.cache import cache
from main.settings import CURRENCY
import string, random, json
from .tasks import send_mail_task
from datetime import datetime


FLIGHT_DATA = {
    'exists': False,
    'destination': '',
    'datetime': '',
    'passengers': '',
    'password': None,
    'currency': CURRENCY,
    'lunch': False,
    'luggage': False,
    'seat_class': 'economy',
    'total_price': 0
}

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
    if request.user.is_authenticated:
        return redirect('cabinet')
    if not request.session.session_key:
        request.session.save()
    key = request.session.session_key
    data = {}
    data['destination'] = [i['destination__name'] for i in Flight.objects.all().values('destination__name').distinct()]
    cities = City.objects.all()
    flight_data = cache.get(key) if cache.get(key) else FLIGHT_DATA
    if request.method == 'GET':
        return render(request, 'first_step.html', {'data':data, 'flight_data':flight_data})
    if request.method == 'POST':
        flight_data['destination'] = request.POST.get('destination')
        flight_data['datetime'] = request.POST.get('datetime')
        flight_data['passengers'] = request.POST.get('passengers')
        cache.set(key, flight_data)
        return redirect(reverse('second_step'))


def second_step(request):
    key = request.session.session_key
    flight_data = cache.get(key) if cache.get(key) else FLIGHT_DATA
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
        flight_data['lunch'] = True if 'lunch' in request.POST else False
        flight_data['luggage'] = True if 'luggage' in request.POST else False
        flight_data['seat_class'] = request.POST['seat_class']
        flight_data['total_price'] = total_price(flight_data)
        cache.set(key, flight_data)
        return redirect(reverse('third_step'))


def third_step(request):
    key = request.session.session_key
    flight_data = cache.get(key) if cache.get(key) else FLIGHT_DATA
    if request.method == 'GET':
        return render(request, 'third_step.html', {'flight_data':flight_data})
    if request.method == 'POST':
        flight_data['first_name'] = request.POST['first_name']
        flight_data['last_name'] = request.POST['last_name']
        flight_data['email'] = request.POST['email']
        flight_data['username'] = request.POST['email']
        try:
            flight_data['password'] = get_random_password()
            user = User.objects.create_user(username=flight_data['username'], email=flight_data['email'],
                                       first_name=flight_data['first_name'], last_name=flight_data['last_name'],
                                       is_active=True, password=flight_data['password'])
            send_mail_task.delay(flight_data)
            cache.set(key, flight_data)
            return render(request, 'user.html', flight_data)
        except:
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
    key = request.session.session_key
    flight_data = cache.get(key) if cache.get(key) else FLIGHT_DATA
    if request.method == 'GET':
        data = {}
        seat_class = SeatClass.objects.all()
        option = Option.objects.all()
        data['destination'] = [i['destination__name'] for i in Flight.objects.all().values('destination__name').distinct()]
        for i in seat_class:
            data[i.name] = i.price
        for i in option:
            data[i.name] = i.price
        return render(request, 'checkin.html', {'data':data, 'flight_data':flight_data})
    if request.method == 'POST':
        flight_data['exists'] = True
        flight_data['destination'] = request.POST.get('destination')
        flight_data['datetime'] = datetime.strptime(request.POST.get('datetime'), '%d.%m.%Y %H:%M:%S')
        flight_data['passengers'] = request.POST.get('passengers')
        flight_data['lunch'] = True if 'lunch' in request.POST else False
        flight_data['luggage'] = True if 'luggage' in request.POST else False
        flight_data['seat_class'] = SeatClass.objects.get(name=request.POST['seat_class'])
        city = City.objects.get(name=flight_data['destination'])
        flight_data['flight'] = Flight.objects.get(destination=city, datetime=flight_data['datetime'])
        flight_data['gate'] = flight_data['flight'].gate
        flight_data['user'] = request.user
        flight_data['name_passenger'] = f'{request.user.first_name} {request.user.last_name}'
        flight_data['total_price'] = total_price(flight_data)
        temp = {i:j for i,j in flight_data.items() if i not in ['exists', 'destination', 'password', 'currency']}
        Ticket.objects.create(**temp)
        cache.set(key, flight_data)
        return render(request, 'ticket.html', {'flight_data':flight_data})


def total_price(flight_data):
    price = flight_data['seat_class'].price
    if flight_data['lunch']:
        price += Option.objects.get(name='lunch').price
    if flight_data['luggage']:
        price += Option.objects.get(name='luggage').price
    return price * int(flight_data['passengers'])


def get_flight_date(request):
    if request.method == 'POST':
        if request.is_ajax():
            try:
                destination = json.load(request).get('destination')
                city = City.objects.get(name=destination)
                l = [i['datetime'].strftime('%d.%m.%Y %H:%M:%S') for i in Flight.objects.filter(destination=city).values('datetime')]
                return JsonResponse(l, safe=False)
            except:
                return JsonResponse({}, safe=False)
    return HttpResponseNotFound()


def count_total_price(request):
    if request.method == 'POST':
        if request.is_ajax():
            d = {}
            key = request.session.session_key
            flight_data = cache.get(key)
            d['passengers'] = flight_data['passengers'] if flight_data else 1
            for i in SeatClass.objects.all():
                d[i.name] = i.price
            for i in Option.objects.all():
                d[i.name] = i.price
            return JsonResponse(d, safe=False)
    return HttpResponseNotFound()
