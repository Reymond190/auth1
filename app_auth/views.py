from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, ProfileAddForm, AddDeviceform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages
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
    form2 = AddDeviceform
    context = {'form':form,"form2":form2}
    if request.method == 'POST' and 'button-name1' in request.POST:
        form = ProfileAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile is updated!')
    if request.method == 'POST' and 'button-name2' in request.POST:
        form2 = AddDeviceform(request.POST)
        if form.is_valid():
            form2.save()
            messages.success(request, 'Device Added')
    return render(request,'main/profile.html',context)

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

    def get_api():
        time2 = datetime.datetime.now()
        time1 = time2 + timedelta(minutes=-5)
        time1 = time1.strftime("%Y-%m-%d %H:%M:00")
        time2 = time2.strftime("%Y-%m-%d %H:%M:00")
        time1 = str(time1)
        time2 = str(time2)
        r1 = requests.get('https://lnt.tracalogic.co/api/ktrack/larsentoubro/2019-08-20 10:05:00/2019-08-20 10:10:00',
                          auth=HTTPBasicAuth('admin', 'admin'))
        x1 = r1.json()
        x2 = json.dumps(x1)
        y1 = json.loads(x2)
        return y1

    @background(schedule=60)
    def reload_and_store():
        f = open('venv/temp.json', 'w+')
        if f.read() is not None:
            f.truncate(0)
            print('fcuk its running')
        x = get_api()
        json.dump(x, f)
        f.close()


    def get_temp():
        f = open('venv/temp.json', 'r+')
        content = f.read()
        return content


    def get_dataframe(y1):
        df1 = json_normalize(y1["assetHistory"])
        df1['serverTimeStamp'] = pd.to_datetime(df1['serverTimeStamp'])
        df1 = df1.set_index('serverTimeStamp')
        df1['eventTimeStamp'] = pd.to_datetime(df1['eventTimeStamp'])  # total no of vehicles
        df1 = df1.drop_duplicates(['deviceImeiNo'],
                                  keep='first')  # NUMBER OF VEHICLES WITH UNIQUE DEVICEIMEINO/PLATENUMBER
        return df1



    def filter_running(df):
        df2 = df.loc[(df["engine"] == "ON") & (df["speed"] > 0)]  # RUNNING VEHICLES
        return df2

    def filter_idle(df):
        df3 = df.loc[(df["engine"] == "ON") & (df["speed"] == 0)]  # IDLE VEHICLES
        return df3

    def filter_stop(df):
        df4 = df.loc[(df["engine"] == "OFF") & (df["speed"] == 0)]  # STOP_VEHICLES
        return df4

    def myfun1(po):
            lat_list = list(po["latitude"])
            long_list = list(po["longitude"])
            gmaps.configure(api_key="AIzaSyDmXhcX8z4d4GxPxIiklwNvtqxcjZoWsWU")
            fig = gmaps.figure()
            markers = gmaps.marker_layer(list(zip(lat_list, long_list)))
            fig.add_layer(markers)
            data1 = embed_snippet(views=[fig])
            return data1

    def listfun(plate, df):
        df5 = df.loc[df1["plateNumber"] == plate]
        return myfun1(df5)


    def change_frames(r):  # enter required dataframes in this function
        p1 = myfun1(r)
        listpl = r["plateNumber"]
        listsp = r["speed"]
        listdt = r["eventTimeStamp"].dt.strftime("%Y-%m-%d %I:%M:%S %p")
        result = zip(listpl, listdt, listsp)
        return p1, result

    time2 = datetime.datetime.now()
    time1 = time2 + timedelta(minutes=-5)

    reload_and_store(schedule=10)
    temp = get_temp()
    y1 = json.loads(temp)
    df1 = get_dataframe(y1)
    df2 = filter_running(df1)
    df3 = filter_idle(df1)
    df4 = filter_stop(df1)



    if request.method == 'GET' and 'totalbutton' in request.GET:
        # temp = get_temp()
        # y1 = json.loads(temp)
        # df1 = get_dataframe(y1)
        # p1 = myfun1(df1)
        # listpl = df1["plateNumber"]
        # listsp = df1["speed"]
        # listdt = df1["eventTimeStamp"].dt.strftime("%Y-%m-%d %I:%M:%S %p")
        # result = zip(listpl, listdt, listsp)
        # temp = get_temp()
        # y1 = json.loads(temp)
        # df1 = get_dataframe(y1)
        p1, result = change_frames(df1)
    elif request.method == 'GET' and 'runningbutton' in request.GET:
        # p1 = myfun1(df2)
        # listpl = df2["plateNumber"]
        # listsp = df2["speed"]
        # listdt = df2["eventTimeStamp"].dt.strftime("%Y-%m-%d %I:%M:%S %p")
        # result = zip(listpl, listdt, listsp)
        # temp = get_temp()
        # y1 = json.loads(temp)
        # df1 = get_dataframe(y1)
        # df2 = filter_running(df1)
        p1, result = change_frames(df2)

    elif request.method == 'GET' and 'idlebutton' in request.GET:
        # p1 = myfun1(df3)
        # listpl = df3["plateNumber"]
        # listsp = df3["speed"]
        # listdt = df3["eventTimeStamp"].dt.strftime("%Y-%m-%d %I:%M:%S %p")
        # result = zip(listpl, listdt, listsp)
        # temp = get_temp()
        # y1 = json.loads(temp)
        # df1 = get_dataframe(y1)
        # df3 = filter_idle(df1)
        p1, result = change_frames(df3)
    elif request.method == 'GET' and 'stopbutton' in request.GET:
        # p1 = myfun1(df4)
        # listpl = df4["plateNumber"]
        # listsp = df4["speed"]
        # listdt = df4["eventTimeStamp"].dt.strftime("%Y-%m-%d %I:%M:%S %p")
        # result = zip(listpl, listdt, listsp)
        # temp = get_temp()
        # y1 = json.loads(temp)
        # df1 = get_dataframe(y1)
        # df4 = filter_stop(df1)
        p1, result = change_frames(df4)

    else:
        # p1 = myfun1(df1)
        # listpl = df1["plateNumber"]
        # listsp = df1["speed"]
        # listdt = df1["eventTimeStamp"].dt.strftime("%Y-%m-%d %I:%M:%S %p")
        # result = zip(listpl, listdt, listsp)
        # temp = get_temp()
        # y1 = json.loads(temp)
        # df1 = get_dataframe(y1)
        p1, result = change_frames(df1)

    if request.method == 'POST' and 'listbutton' in request.POST:
        # temp = get_temp()
        # y1 = json.loads(temp)
        # df1 = get_dataframe(y1)
        plate = request.POST['listbutton']
        p1 = listfun(plate, df1)
        print(plate)
    else:
        print('escaped if case sorry!!!!')


    total = len(df1)
    running = len(df2)
    idle = len(df3)
    stop = len(df4)
    context = {'vehicle_list': p1,'total':total,'running':running,'idle':idle, 'stop':stop, 'list_plate':result}
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


