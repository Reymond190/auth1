from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, ProfileAddForm, AddDeviceform
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages
from datetime import datetime
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import AddDevice,Profile
from django.views.generic import ListView, DetailView
from requests.auth import HTTPBasicAuth
from ipywidgets.embed import embed_minimal_html, embed_snippet
from vehicles.models import vehicle
import json


from background_task import background
import requests
import gmaps
from datetime import timedelta
import datetime
import pandas as pd
import json as simplejson
from pandas.io.json import json_normalize
import sys
from pandas.io.json import json_normalize
from django.views.decorators.cache import cache_control


def get_api():
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
    return y1


def reload_and_store():
    f = open('venv/temp.json', 'w+')
    if f.read() is not None:
        f.truncate(0)
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


def myfun1(po):             #argument:dataframe(df)
    lat_list = list(po["latitude"])
    long_list = list(po["longitude"])
    gmaps.configure(api_key="AIzaSyDmXhcX8z4d4GxPxIiklwNvtqxcjZoWsWU")
    fig = gmaps.figure()
    var1 = json.dumps(
        [{'lat': country, 'lng': wins} for country, wins in zip(lat_list, long_list)]
    )
    markers = gmaps.marker_layer(list(zip(lat_list, long_list)))
    fig.add_layer(markers)
    data1 = embed_snippet(views=[fig])
    return data1,var1


def myfunpro(po):             #argument:dataframe(df)
    lat_list = list(po["latitude"])
    long_list = list(po["longitude"])
    gmaps.configure(api_key="AIzaSyDmXhcX8z4d4GxPxIiklwNvtqxcjZoWsWU")
    fig = gmaps.figure()
    var1 = json.dumps(
        [{'lat': country, 'lng': wins} for country, wins in zip(lat_list, long_list)]
    )
    return var1


def listfun(plate, df):
    df5 = df.loc[df["plateNumber"] == plate]
    return myfun1(df5)

def listfun2(plate, df):
    df5 = df.loc[df["plateNumber"] == plate]
    return df5

# def get_single_loco(plate,df):
#     df5 = df.loc[df["plateNumber"] == plate]
#     lat_list = list(df5["latitude"])
#     long_list = list(df5["longitude"])
#     p = lat_list[0]
#     q = long_list[0]
#     r = p+q
#     r = str(r)
#     return r


def change_frames(r):  # enter required dataframes in this function
    p1,v1 = myfun1(r)
    listpl = r["plateNumber"]
    listsp = r["speed"]
    listdt = r["eventTimeStamp"].dt.strftime("%Y-%m-%d %I:%M:%S %p")
    result = zip(listpl, listdt, listsp)
    return p1, result

def get_details(r):
    plateno = r["plateNumber"]
    # time = r["serverTimeStamp"]
    speed = r["speed"]
    latitude = r["latitude"]
    longitude = r["longitude"]
    lat = str(latitude)
    log = str(longitude)
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="geoapp")
    location = geolocator.reverse("52.509669, 13.376294")

    engine = r["engine"]
    status = r["status"]

    odometer = r["odometer"]
    assetcode = r["AssetCode"]
    direction = r["direction"]
    result = zip(plateno, speed,engine,status,latitude,longitude,odometer,assetcode,direction,location)
    return result




# ------------------------------------------------------------main-----------------------------------------------------------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def start(request):
    return render(request, 'file1.html')

def detail(request):
    queryset = vehicle.objects.all()
    temp = get_temp()
    y1 = json.loads(temp)
    df1 = get_dataframe(y1)
    df2 = filter_running(df1)
    df3 = filter_idle(df1)
    df4 = filter_stop(df1)
    total = len(df1)
    running = len(df2)
    idle = len(df3)
    stop = len(df4)
    context = {"object_list":queryset,'total':total,'running':running,'idle':idle, 'stop':stop,}
    return render(request, 'main/details.html',context)
def tickets(request):
    return render(request,'main/tickets.html')

def alerts(request):
    return render(request,'main/alerts.html')

def setting(request):
    return render(request,'main/settings.html')

def tour(request):
    return render(request,'main/tour.html')

class devicelistview(ListView):
    queryset = AddDevice.objects.all()
    template_name = 'main/class.html'


    def get_queryset(self,*args,**kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        return AddDevice.objects.filter(pk=pk)



def device_listview(request,pk,*args,**kwargs):
    queryset = AddDevice.objects.get(pk=pk)
    instance = AddDevice.objects.get_by_id(pk)
    print(instance)
    # instance = get_object_or_404(AddDevice,id=pk)
    print(pk)
    print(id)
    context = {
        'object_list':queryset
    }
    return render(request,"main/class.html",context)



def geofence(request):
    temp = get_temp()
    y1 = json.loads(temp)
    df1 = get_dataframe(y1)
    y1,result = change_frames(df1)

    if request.method == 'POST' and 'listbutton1' in request.POST:
        plate = request.POST['listbutton1']
        p1, v1 = listfun(plate, df1)

    else:
        print('escaped if case on geofence!!!!')
        v1 = "{lat: 28.7041, lng: 77.1025}"
    context = {'plateloco':v1,
               'list_plate':result}
    print(v1)
    return render(request, 'main/geofence.html', context)

def marker(request):
    return render(request, 'main/marker.html')

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
    context = {'form':form, "form2":form2}
    if request.method == 'POST' and 'button-name1' in request.POST:
        form = ProfileAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile is updated!')
    if request.method == 'POST' and 'button-name2' in request.POST:
        form2 = AddDeviceform(request.POST)
        if form2.is_valid():
            print("getting inside if")
            fs = form2.save(commit=False)
            fs.user = request.user
            fs.save()
            print("save")
        messages.success(request, 'Device Added')
    return render(request,'main/profile.html',context)


# @background(schedule=10)
# def notify_user(pk):
#     idle = pk
#     idle= idle +1
#     return idle


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def map (request):

    # time2 = datetime.datetime.now()
    # time1 = time2 + timedelta(minutes=-5)
    # reload_and_store()

    temp = get_temp()
    y1 = json.loads(temp)
    df1 = get_dataframe(y1)
    df2 = filter_running(df1)
    df3 = filter_idle(df1)
    df4 = filter_stop(df1)



    if request.method == 'GET' and 'totalbutton' in request.GET:
        p1, result = change_frames(df1)
        p1, v1 = myfun1(df1)
    elif request.method == 'GET' and 'runningbutton' in request.GET:
        p1, result = change_frames(df2)
        p1, v1 = myfun1(df2)
    elif request.method == 'GET' and 'idlebutton' in request.GET:
        p1, result = change_frames(df3)
        p1, v1 = myfun1(df3)
    elif request.method == 'GET' and 'stopbutton' in request.GET:
        p1, result = change_frames(df4)
        p1, v1 = myfun1(df4)

    else:
        p1, result = change_frames(df1)
        p1, v1 = myfun1(df1)

    if request.method == 'POST' and 'listbutton' in request.POST:
        plate = request.POST['listbutton']
        p1, v1 = listfun(plate, df1)
        one = listfun2(plate, df1)
        two = get_details(one)
        print(plate)
    else:
        print('escaped if case sorry!!!!')


    total = len(df1)
    running = len(df2)
    idle = len(df3)
    stop = len(df4)
    context = {'myfile':v1,'total':total,'running':running,'idle':idle, 'stop':stop, 'list_plate':result}
    return render(request, 'main/track.html', context)

def funclu(po):             #argument:dataframe(df)
    lat_list = list(po["latitude"])
    long_list = list(po["longitude"])
    v_plate = list(po["plateNumber"])
    v_status = list(po["status"])
    gmaps.configure(api_key="AIzaSyDmXhcX8z4d4GxPxIiklwNvtqxcjZoWsWU")
    fig = gmaps.figure()
    var1 = json.dumps(
        [{'lat': country, 'lng': wins,'plate':num,'status':v_sta} for country, wins, num, v_sta in zip(lat_list, long_list,v_plate,v_status)]
    )
    markers = gmaps.marker_layer(list(zip(lat_list, long_list)))
    fig.add_layer(markers)
    data1 = embed_snippet(views=[fig])
    return data1,var1

def cluster(request):
    temp = get_temp()
    y1 = json.loads(temp)
    df1 = get_dataframe(y1)
    df2 = filter_running(df1)
    df3 = filter_idle(df1)
    df4 = filter_stop(df1)
    total = len(df1)
    running = len(df2)
    idle = len(df3)
    stop = len(df4)
    p1, result = funclu(df1)
    queryset = vehicle.objects.all()

    context = {
        "myfile":result,'total':total,'running':running,'idle':idle, 'stop':stop,"object_list":queryset
    }

    return render(request, 'main/cluster.html',context)

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

def table_map(request):

    return render("main/table_map.html")

