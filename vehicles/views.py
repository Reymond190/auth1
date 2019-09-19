from django.shortcuts import render
from .models import vehicle
import names
import pandas as pd
import random
from pandas.io.json import json_normalize
import json
import names
from googlegeocoder import GoogleGeocoder
from django import template



def get_dataframe(y1):
    df1 = json_normalize(y1["assetHistory"])
    df1['serverTimeStamp'] = pd.to_datetime(df1['serverTimeStamp'])
    df1 = df1.set_index('serverTimeStamp')
    df1['eventTimeStamp'] = pd.to_datetime(df1['eventTimeStamp'])  # total no of vehicles
    df1 = df1.drop_duplicates(['deviceImeiNo'],
                              keep='first')
    p = df1.to_dict()
    print(type(p))
    print(p)
    return p

def auto(request):
    f = open('venv/temp.json', 'r+')
    temp = f.read()
    y1 = json.loads(temp)

    print(len(y1["assetHistory"]))
    df1 = json_normalize(y1["assetHistory"])
    df1['serverTimeStamp'] = pd.to_datetime(df1['serverTimeStamp'])
    df1 = df1.set_index('serverTimeStamp')
    df1['eventTimeStamp'] = pd.to_datetime(df1['eventTimeStamp'])  # total no of vehicles
    df1 = df1.drop_duplicates(['deviceImeiNo'], keep='first').to_dict('records')
    print(len(df1))
    print(df1[0]["speed"])
    print(type(df1))
    geocoder = GoogleGeocoder("AIzaSyDmXhcX8z4d4GxPxIiklwNvtqxcjZoWsWU")
    y1 = df1

    for i in range(0,256):
        v1 = vehicle()
        print(i)
        name = names.get_first_name()
        v1.name = name
        speed = str(y1[i]["speed"])
        v1.speed = speed
        latitude = y1[i]["latitude"]
        v1.latitude = latitude
        longitude = y1[i]["longitude"]
        v1.longitude = longitude
        location = geocoder.get((latitude, longitude))
        print(location[0])
        p = str(location[0])
        v1.location = p
        engine = str(y1[i]["engine"])
        v1.engine = engine
        status = str(y1[i]["status"])
        v1.status = status
        odometer = str(y1[i]["odometer"])
        pl = str(y1[i]["plateNumber"])
        v1.plateNumber = pl
        imei = str(y1[i]["deviceImeiNo"])
        v1.deviceImeiNo = imei
        assetid = str(y1[i]["assetId"])
        v1.assetId = assetid
        compid = str(y1[i]["companyId"])
        v1.companyId = compid
        v1.odometer = odometer
        assetcode = str(y1[i]["AssetCode"])
        v1.assetId = assetcode
        direction = str(y1[i]["direction"])
        v1.direction = direction
        v1.save()
    return render(request,'main/new.html')


