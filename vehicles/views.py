from django.shortcuts import render
from .models import vehicle
import names
import pandas as pd
from pandas.io.json import json_normalize
import json
import names
from googlegeocoder import GoogleGeocoder

res_list = []



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
    x1 = json.dumps(temp)
    y1 = json.loads(x1)
    print(len(y1))
    print(type(y1))
    # t = get_dataframe(y1)
    # for i in range(len(y1["assetHistory"])):
    #     s = str(y1["assetHistory"][i]["plateNumber"])
    #     t  = str(y1["assetHistory"][i + 1:]["plateNumber"])
    #     if s == t:
    #         pass
    #     else:
    #         res_list.append(y1["assetHistory"][i])

    print(len(res_list))

    geocoder = GoogleGeocoder("AIzaSyDmXhcX8z4d4GxPxIiklwNvtqxcjZoWsWU")


    for i in range(58,100):
        v = vehicle()
        print(i)
        name = names.get_first_name()
        v.name = name
        speed = str(y1["assetHistory"][i]["speed"])
        v.speed = speed
        latitude = y1["assetHistory"][i]["latitude"]
        v.latitude = latitude
        longitude = y1["assetHistory"][i]["longitude"]
        v.longitude = longitude
        location = geocoder.get((latitude, longitude))
        print(location[0])
        engine = str(y1["assetHistory"][i]["engine"])
        v.engine = engine
        status = str(y1["assetHistory"][i]["status"])
        v.status = status
        odometer = str(y1["assetHistory"][i]["odometer"])
        pl = str(y1["assetHistory"][i]["plateNumber"])
        v.plateNumber = pl
        imei = str(y1["assetHistory"][i]["deviceImeiNo"])
        v.deviceImeiNo = imei
        assetid = str(y1["assetHistory"][i]["assetId"])
        v.assetId = assetid
        compid = str(y1["assetHistory"][i]["companyId"])
        v.companyId = compid
        v.odometer = odometer
        assetcode = str(y1["assetHistory"][i]["AssetCode"])
        v.assetId = assetcode
        direction = str(y1["assetHistory"][i]["direction"])
        v.direction = direction
        v.save()
    return render(request,'main/new.html')


