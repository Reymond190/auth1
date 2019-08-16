from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, ProfileAddForm, AddDeviceform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
from datetime import datetime
from requests.auth import HTTPBasicAuth
from ipywidgets.embed import embed_minimal_html, embed_snippet
import json
from background_task import background
import requests
import gmaps
from datetime import timedelta
import datetime
import pandas as pd
from pandas.io.json import json_normalize
import sys
from pandas.io.json import json_normalize
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def start(request):
    return render(request, 'file1.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def reports(request):
    return render(request, 'main/report.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username= username, password = password)
            # messages.success(request,f'Your account has been created {username}! Login to continue!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def profile(request):
    form = ProfileAddForm
    if request.method == 'POST':
        form = ProfileAddForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'main/profile.html',{'form':form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def AddDevice(request):
    form = AddDeviceform
    if request.method == 'POST':
        form = AddDeviceform(request.POST)
        if form.is_valid():
            return start
    return render(request,'registration/Add.html',{'form':form})

# @background(schedule=10)
# def notify_user(pk):
#     idle = pk
#     idle= idle +1
#     return idle

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def map (request):
    time2 = datetime.datetime.now()
    time1 = time2 + timedelta(minutes=-5)
    time1 = time1.strftime("%Y-%m-%d %H:%M:00")
    time2 = time2.strftime("%Y-%m-%d %H:%M:00")
    time1 = str(time1)
    time2 = str(time2)
    r1 = requests.get('https://lnt.tracalogic.co/api/ktrack/larsentoubro/' + time1 + '/' + time2,
                      auth=HTTPBasicAuth('admin', 'admin'))
    x1 = r1.json()
    x2 = json.dumps(x1)
    y1 = json.loads(x2)
    df1 = json_normalize(y1["assetHistory"])
    df1['serverTimeStamp'] = pd.to_datetime(df1['serverTimeStamp'])
    df1 = df1.set_index('serverTimeStamp')
    df1['eventTimeStamp'] = pd.to_datetime(df1['eventTimeStamp'])
    print("TOTAL API'S COUNT WITHIN 5 MINUTES TODAY = ", len(df1))
    # NUMBER OF VEHICLES WITH UNIQUE DEVICEIMEINO/PLATENUMBER
    df1 = df1.drop_duplicates(['deviceImeiNo'], keep='first')
    print("BY REMOVING DUPICATES, TOTAL NUMBER_OF_VEHICLES = ", len(df1))
    df2 = df1.loc[(df1["engine"] == "ON") & (df1["speed"] > 0)]
    print("\nNUMBER OF RUNNING_VEHICLES ", len(df2))
    df3 = df1.loc[(df1["engine"] == "ON") & (df1["speed"] == 0)]
    print("\nNumber of IDLE_VEHICLES ", len(df3))
    df4 = df1.loc[(df1["engine"] == "OFF") & (df1["speed"] == 0)]
    print("\nNumber of STOP_VEHICLES ", len(df4))
    lat_list = list(df2["latitude"])
    long_list = list(df2["longitude"])
    gmaps.configure(api_key="AIzaSyDmXhcX8z4d4GxPxIiklwNvtqxcjZoWsWU")
    fig = gmaps.figure()
    markers = gmaps.marker_layer(list(zip(lat_list, long_list)))
    fig.add_layer(markers)
    data1 = embed_snippet(views=[fig])
    total = len(df1)
    running = len(df2)
    idle = len(df3)
    stop = len(df4)
    context = {'data': data1,'total':total,'running':running,'idle':idle,'stop':stop}
    return render(request, 'main/track.html', context)





class charts(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/in.html')

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
     r = requests.get(' https://lnt.tracalogic.co/api/ktrack/larsentoubro/2019-08-07 11:00:00/2019-08-07 11:05:00 ',
                      auth=HTTPBasicAuth('admin', 'admin'))
     x = r.json()
     x1 = json.dumps(x)
     y = json.loads(x1)
     df = json_normalize(y["assetHistory"])
     df['serverTimeStamp'] = pd.to_datetime(df['serverTimeStamp'])
     df = df.set_index('serverTimeStamp')
     df['eventTimeStamp'] = pd.to_datetime(df['eventTimeStamp'])
     df1 = df.drop_duplicates(['deviceImeiNo'], keep='last')
     data = {
            "labels": ["Vechicle_On", "Vechicle_Off"],
            "data": [len(df1.loc[df1['engine']=="ON"]), len(df1.loc[df1['engine']=="OFF"])],
        }
     return Response(data)

class BarChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        r = requests.get(' https://lnt.tracalogic.co/api/ktrack/larsentoubro/2019-08-07 11:00:00/2019-08-07 11:05:00 ',
                         auth=HTTPBasicAuth('admin', 'admin'))
        x = r.json()
        x1 = json.dumps(x)
        y = json.loads(x1)
        df = json_normalize(y["assetHistory"])
        df['serverTimeStamp'] = pd.to_datetime(df['serverTimeStamp'])
        df = df.set_index('serverTimeStamp')
        df['eventTimeStamp'] = pd.to_datetime(df['eventTimeStamp'])
        df1 = df.drop_duplicates(['deviceImeiNo'], keep='last')

        s = df1["speed"].value_counts()


        data = {
            "labels": [df1['speed']],
            "data": [s],
        }
        return Response(data)

class Doughnut(APIView):
        authentication_classes = []
        permission_classes = []

        def get(self, request, format=None):
            r = requests.get(
                ' https://lnt.tracalogic.co/api/ktrack/larsentoubro/2019-08-07 11:00:00/2019-08-07 11:05:00 ',
                auth=HTTPBasicAuth('admin', 'admin'))
            x = r.json()
            x1 = json.dumps(x)
            y = json.loads(x1)
            df = json_normalize(y["assetHistory"])
            df['serverTimeStamp'] = pd.to_datetime(df['serverTimeStamp'])
            df = df.set_index('serverTimeStamp')
            df['eventTimeStamp'] = pd.to_datetime(df['eventTimeStamp'])
            df1 = df.drop_duplicates(['deviceImeiNo'], keep='last')

            data = {
                "labels": ["Delhi", "Maharashtra"],
                "data": [len(df1.loc[df1['engine'] == "ON"]), len(df1.loc[df1['engine'] == "OFF"])],
            }
            return Response(data)


class track(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        time2 = datetime.datetime.now()
        time1 = time2 + timedelta(minutes=-5)
        time1 = time1.strftime("%Y-%m-%d %H:%M:00")
        time2 = time2.strftime("%Y-%m-%d %H:%M:00")

        time1 = str(time1)
        time2 = str(time2)
        r = requests.get('https://lnt.tracalogic.co/api/ktrack/larsentoubro/' + time1 + '/' + time2,
                         auth=HTTPBasicAuth('admin', 'admin'))
        x = r.json()
        x1 = json.dumps(x)
        y = json.loads(x1)
        latitudes = []
        longitudes = []
        for i in range(len(y["assetHistory"])):
            latitudes.append(y["assetHistory"][i]["latitude"])
            longitudes.append(y["assetHistory"][i]["longitude"])
        print(len(latitudes))
        print(len(longitudes))
        data = {

            "data" : [latitudes , longitudes],
        }
        return Response(data)


