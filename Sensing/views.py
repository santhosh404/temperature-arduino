from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login as Login, logout as Logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from .forms import SignUpForm
from django.http import response, JsonResponse
from .models import *
import string
import random
import json
from datetime import datetime
import pytz


def get_date():
    tz_NY = pytz.timezone('Asia/Kolkata')
    datetime_NY = datetime.now(tz_NY)
    date, time = (datetime_NY.strftime("%Y-%m-%d %H:%M:%S")).split()
    return date, time


def get_apilist():
    a = []
    for i in Table1.objects.values('api'):
        a.append(i['api'])
    return a


def register(request):
    Rform = SignUpForm()
    if request.method == "POST":
        Rform = UserCreationForm(request.POST)
        if Rform.is_valid():
            api = Generate_api()
            user = User.objects.last()
            api = Generate_api()
            b = Table1(reference_id=user.id+1, api=api)
            b.save()
            Rform.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            form = SignUpForm()
            return render(request, 'register.html', {"error": "signup failed!", "Rform": Rform})

    return render(request, "register.html", {"Rform": Rform})


def login(request):
    if request.method == "POST":
        username = request.POST['name']
        password = request.POST['password']
        authen = authenticate(request, username=username, password=password)

        if authen is not None:
            Login(request, authen)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, "login.html", context={"mess": "Username or Password Incorrect!"})

    return render(request, "login.html")


def Generate_api(length=16):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def home(request):
    if request.user.is_authenticated:
        data = Table1.objects.filter(reference_id=request.user.id)
        return render(request, "home.html", {'data': data})
    return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def data(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        if received_json_data['API'] in get_apilist():
            dat, tim = get_date()
            noob = Data.objects.create(
                api_key=Table1.objects.get(api=received_json_data['API']),
                temparature=received_json_data['Temperature'],
                humidity=received_json_data['Humidity'],
                dat=dat,
                tim=tim
            )

        else:
            return HttpResponse("Invalid API.")
    return HttpResponseRedirect(reverse('home'))


def visualize(request):
    if request.user.is_authenticated:
        data_objs = Data.objects.filter(
            api_key=Table1.objects.get(reference_id=request.user.id))
        length = len(data_objs)
        if len(data_objs) == 0:
            return render(request, "viz.html", {'record': 'No Records Found.', 'length': str(length)})
        else:
            try:

                data = []

                for i in data_objs:
                    temp_data = {
                        "temperature": i.temparature,
                        "humidity": i.humidity,
                        "dat": str(i.dat),
                        "tim": str(i.tim)
                    }

                    data.append(temp_data)
                Temperature = json.dumps(data)
                return render(request, "viz.html", {"data": data,  'length': length})

            except ObjectDoesNotExist:
                return HttpResponse("No Records found.")
    return HttpResponseRedirect(reverse('home'))


def logout_view(request):
    Logout(request)
    return HttpResponseRedirect(reverse('login'))
