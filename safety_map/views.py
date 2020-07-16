from django.shortcuts import render
from safety_map.models import SafetyZone
import folium
import urllib.request
import datetime
import time
import json
import webbrowser
import pymysql
import numpy as np
import pandas as pd
import point
import geodaisy.converters as convert
from plpygis import Geometry
# Create your views here.
def home(request):
    return render(request, 'home.html')

def startpage(request):
    return render(request, 'startpage.html')

def showMaps(request):
    map = folium.Map(location=[37.6511988,127.0161604],zoom_start=12)
    maps=map._repr_html_() 
    return render(request, 'home.html',{'map':maps})

#한정원 : 안심장소 안전벨 테스트 100개 
def filter_safetyzone_bell(request): # 한정원
    map = folium.Map(location=[37.6511988,127.0161604],zoom_start=12)
    #folium.Marker([37.566345, 126.977893],popup='seouloffice').add_to(map) #테스트로 추가한 서울시청 마커
    for i in range(1,101):
        bell_ob = SafetyZone.objects.get(safety_zone_pk=i)
        bell_ob_geo = Geometry(bell_ob.safety_loc.hex()[8:])
        bell_ob_geo_con = convert.wkt_to_geojson(str(bell_ob_geo.shapely))
        bell_ob_dict = json.loads(bell_ob_geo_con)
        folium.Marker([bell_ob_dict['coordinates'][0],bell_ob_dict['coordinates'][1]],popup='bell').add_to(map)
    maps = map._repr_html_()
    return render(request,'home.html',{'map':maps})

def mypage(request):
    return render(request, 'mypage.html')

def manage_alarm(request):
    return render(request, 'manage_alarm.html')

def manage_danger_map(request):
    return render(request, 'manage_danger_map.html')

def manage_protecter(request):
    return render(request, 'manage_protecter.html')

def danger_map(request):
    return render(request, 'danger_map.html')

def register_danger(request):
    return render(request, 'register_danger.html')
