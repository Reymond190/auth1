from django.shortcuts import render
from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from vehicles.models import vehicle
from datetime import date
import json
from app_auth.views import get_temp,get_dataframe,listfun


def travel_summary(request):
    queryset = vehicle.objects.all()
    context = {"object_list":queryset}
    return render(request, 'reports/travel_summary.html',context)


import datetime



def detail_travel_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/travel_detail_summary.html',context)

def trip_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/trip_summary.html',context)


def stoppage_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/stoppage_summary.html',context)

def idle_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/idle_summary.html',context)

def idle_detail_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/idle_detail_summary.html',context)

def inactive_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/inactive_summary.html',context)

def ignition_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/ignition_summary.html',context)

def ac_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/ac_summary.html',context)

def ac_misused_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/ac_misused_summary.html',context)

def speed_vs_distance(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/speed_vs_distance.html',context)

def vehicle_location(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/vehicle_location.html',context)

def sms_email(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/sms_email.html',context)

def vehicle_status(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/vehicle_status.html',context)

def system_log(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/system_log.html',context)

def device_log(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/device_log.html',context)

def analog_data(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/analog_data.html',context)

def personal_report(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/personal_report.html',context)

def report_generator(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/travel_detail_summary.html',context)


def actual_trip_summary(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/actual_trip_summary.html',context)

def rfid_data(request):
    queryset = vehicle.objects.all()
    x = datetime.datetime.now()
    p = x.date()
    print(p)
    context = {"object_list":queryset,'date':p}
    return render(request, 'reports/rfid_data.html',context)

