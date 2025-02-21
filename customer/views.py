import logging
from dataclasses import dataclass, asdict
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from customer.models import User, City, Option, SeatClass, Flight, Ticket, SeatNumber
from django.core.cache import cache
import string
import random
import json
from .tasks import send_mail_task
from datetime import datetime


logger = logging.getLogger(__name__)


@dataclass
class FlightData():
    destination: str = ''
    datetime: datetime = None
    flight: Flight = None
    gate: str = ''
    seat_class: SeatClass = None
    seat: SeatNumber = None
    lunch: bool = False
    luggage: bool = False
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    ticket_code: str = ''
    user: User = None
    total_price: float = 0.00
    error: str = ''


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


def get_random_string():
    str = string.ascii_letters + string.digits
    return ''.join([random.choice(str) for i in range(8)])


def first_step(request):
    if request.user.is_authenticated:
        return redirect('cabinet')

    if not request.session.session_key:
        request.session.save()

    key = request.session.session_key
    flight_data = cache.get(key)
    if not flight_data:
        flight_data = FlightData()

    if request.method == 'GET':
        data = {}
        data['destination'] = [i['destination__name'] for i in Flight.objects.all().values('destination__name').distinct()]
        cities = City.objects.all()
        return render(request, 'first_step.html', {'data': data, 'flight_data': flight_data})

    if request.method == 'POST':
        try:
            date_time = datetime.strptime(request.POST.get('datetime'), '%d.%m.%Y %H:%M:%S')
        except ValueError:
            flight_data.error = 'Wrong Datetime'
            cache.set(key, flight_data)
            return redirect(reverse('first_step'))

        city = City.objects.filter(name=request.POST.get('destination')).first()
        if city:
            flight_data.destination = city.name
            flight = Flight.objects.filter(destination=city, datetime=date_time).first()
            if flight:
                flight_data.datetime = date_time
                flight_data.flight = flight
                cache.set(key, flight_data)
                return redirect(reverse('second_step'))
            else:
                flight_data.error = 'Wrong Datetime'
                cache.set(key, flight_data)
                return redirect(reverse('first_step'))
        else:
            flight_data.error = 'Wrong Destination'
            cache.set(key, flight_data)
            return redirect(reverse('first_step'))


def second_step(request):
    key = request.session.session_key
    flight_data = cache.get(key)
    if not flight_data:
        return redirect(reverse('first_step'))

    if request.method == 'GET':
        data = {}
        seat_class = SeatClass.objects.all()
        option = Option.objects.all()
        for i in seat_class:
            data[i.name] = i.price
        for i in option:
            data[i.name] = i.price
        logger.info(f'Data for second step: {data}')
        return render(request, 'second_step.html', {'data': data, 'flight_data': flight_data})

    if request.method == 'POST':
        flight_data.lunch = True if 'lunch' in request.POST else False
        flight_data.luggage = True if 'luggage' in request.POST else False
        flight_data.seat_class = SeatClass.objects.get(name=request.POST['seat_class'])
        seat = SeatNumber.objects.filter(
            airplane=flight_data.flight.airplane,
            seat_class=flight_data.seat_class,
            number=request.POST.get('available_seat')
        ).first()
        if seat:
            flight_data.seat = seat
            flight_data.gate = flight_data.flight.gate
            flight_data.total_price = total_price(flight_data)
            cache.set(key, flight_data)
            return redirect(reverse('third_step'))
        else:
            flight_data.error = 'Wrong seat number'
            cache.set(key, flight_data)
            return redirect(reverse('second_step'))


def third_step(request):
    key = request.session.session_key
    logger.info(f'Key: {key}')
    flight_data = cache.get(key)
    if not flight_data:
        return redirect(reverse('second_step'))
    if request.method == 'GET':
        return render(request, 'third_step.html', {'flight_data': flight_data})
    if request.method == 'POST':
        flight_data.first_name = request.POST['first_name']
        flight_data.last_name = request.POST['last_name']
        flight_data.email = request.POST['email']
        flight_data.ticket_code = hash(
            flight_data.email + flight_data.first_name + flight_data.last_name + str(flight_data.flight.id)
        )
        try:
            flight_data.password = get_random_string()
            user = User.objects.create_user(
                username=flight_data.email, email=flight_data.email,
                is_active=True, password=flight_data.password
            )
            flight_data.user = user
            new_user = True
        except:
            flight_data.user = User.objects.get(username=flight_data.email)
            new_user = False
        flight_data_dict = asdict(flight_data)
        temp = {
            i: j for i, j in flight_data_dict.items()
            if i not in ['destination', 'password', 'currency', 'email', 'username', 'error']
        }
        logger.info(f'Flight data: {flight_data_dict}')
        if not Ticket.objects.filter(ticket_code=flight_data.ticket_code).exists():
            Ticket.objects.create(**temp)
        cache.set(key, flight_data)
        response = render(request, 'ticket.html', {'flight_data': flight_data_dict, 'new_user': new_user})
        return response
        send_mail_task.delay(flight_data.email, response.content.decode('utf-8'))
        return render(request, 'user.html', {'flight_data': flight_data_dict, 'new_user': new_user})


@login_required(login_url='/signin/')
def checkin(request):
    key = request.session.session_key
    flight_data = cache.get(key)
    if not flight_data:
        flight_data = FlightData()

    if request.method == 'GET':
        data = {}
        seat_class = SeatClass.objects.all()
        option = Option.objects.all()
        data['destination'] = [i['destination__name'] for i in Flight.objects.all().values('destination__name').distinct()]
        for i in seat_class:
            data[i.name] = i.price
        for i in option:
            data[i.name] = i.price
        return render(request, 'checkin.html', {'data': data, 'flight_data': flight_data})

    if request.method == 'POST':
        flight_data.first_name = request.POST['first_name']
        flight_data.last_name = request.POST['last_name']
        try:
            date_time = datetime.strptime(request.POST.get('datetime'), '%d.%m.%Y %H:%M:%S')
        except ValueError:
            flight_data.error = 'Wrong Datetime'
            cache.set(key, flight_data)
            return redirect(reverse('checkin'))

        flight_data.lunch = True if 'lunch' in request.POST else False
        flight_data.luggage = True if 'luggage' in request.POST else False
        flight_data.seat_class = SeatClass.objects.get(name=request.POST['seat_class'])
        city = City.objects.filter(name=request.POST.get('destination')).first()
        if city:
            flight_data.destination = city.name
            flight = Flight.objects.filter(destination=city, datetime=date_time).first()
            if flight:
                flight_data.datetime = date_time
                flight_data.flight = flight
            else:
                flight_data.error = 'Wrong Datetime'
                cache.set(key, flight_data)
                return redirect(reverse('checkin'))
        else:
            flight_data.error = 'Wrong Destination'
            cache.set(key, flight_data)
            return redirect(reverse('checkin'))

        seat = SeatNumber.objects.filter(airplane=flight_data.flight.airplane, seat_class=flight_data.seat_class,
                                         number=request.POST.get('available_seat')).first()
        if not seat:
            flight_data.error = 'Wrong seat number'
            cache.set(key, flight_data)
            return redirect(reverse('checkin'))
        else:
            flight_data.seat = seat
            flight_data.gate = flight_data.flight.gate
            flight_data.user = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            flight_data.total_price = total_price(flight_data)
            flight_data.ticket_code = hash(flight_data.user.email + flight_data.first_name + flight_data.last_name + str(flight_data.flight.id))
            temp = {i: j for i, j in flight_data.__dict__.items() if i not in [
                'destination', 'password', 'currency', 'email', 'username', 'error']}

            if not Ticket.objects.filter(ticket_code=flight_data.ticket_code).exists():
                Ticket.objects.create(**temp)
            cache.set(key, flight_data)
            return render(request, 'ticket.html', {'flight_data': flight_data})


def total_price(flight_data):
    price = flight_data.seat_class.price
    if flight_data.lunch:
        price += Option.objects.get(name='lunch').price
    if flight_data.luggage:
        price += Option.objects.get(name='luggage').price
    return price


def get_flight_date(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                destination = json.load(request).get('destination')
                city = City.objects.get(name=destination)
                l = [i['datetime'].strftime('%d.%m.%Y %H:%M:%S') for i in Flight.objects.filter(
                    destination=city).values('datetime')]
                return JsonResponse(l, safe=False)
            except Exception as exc:
                logger.error(exc.__str__())
    return JsonResponse({}, status=404)


def count_total_price(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            key = request.session.session_key
            flight_data = cache.get(key)
            d = {}
            for i in SeatClass.objects.all():
                d[i.name] = i.price
            for i in Option.objects.all():
                d[i.name] = i.price
            try:
                d['seat_class'] = flight_data.seat_class.name
            except:
                d['seat_class'] = 'economy'
            return JsonResponse(d, safe=False)
    return JsonResponse({}, status=404)


def available_seat(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                data = json.load(request)
                logger.info(f'Avaliable seat request: {data}')
                try:
                    date_time = datetime.strptime(data['datetime'], '%d.%m.%Y %H:%M:%S')
                except ValueError:
                    pass
                city = City.objects.get(name=data['destination'])
                logger.info(f'City: {city}')
                flight = Flight.objects.get(destination=city, datetime=date_time)
                logger.info(f'Flight: {flight}')
                airplane = flight.airplane
                seat_class = SeatClass.objects.get(name=data['seat_class'])
                logger.info(f'Seat class: {seat_class}')
                seat = SeatNumber.objects.filter(airplane=airplane, seat_class=seat_class).values('number')
                all_seat = [i['number'] for i in seat]
                tickets = Ticket.objects.filter(flight=flight, seat_class=seat_class)
                if tickets:
                    take_seat = [i.seat.number for i in tickets]
                    free_seat = [i for i in all_seat if i not in take_seat]
                    return JsonResponse(free_seat, safe=False)
                else:
                    return JsonResponse(all_seat, safe=False)
            except Exception as exc:
                logger.error(exc.__str__())
    return JsonResponse({}, status=404)


@login_required(login_url='/signin/')
def cabinet(request):
    if request.method == 'GET':
        tickets = Ticket.objects.filter(user=request.user).order_by('create_datetime')
        if tickets:
            return render(request, 'cabinet.html', {'tickets':tickets})
        return render(request, 'cabinet.html', {})
