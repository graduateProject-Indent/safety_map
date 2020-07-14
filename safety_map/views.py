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
# Create your views here.
def home(request):
    return render(request, 'home.html')

def startpage(request):
    return render(request, 'startpage.html')

def showMaps(request):
    map = folium.Map(location=[37.6511988,127.0161604],zoom_start=12)
    maps=map._repr_html_() 
    return render(request, 'home.html',{'map':maps})

#한정원 : 안심장소보기 미완성

def showSafetyZone(request):
    map = folium.Map(location=[37.6511988,127.0161604],zoom_start=12)
    maps = map._repr_html_()
    return render(request,'safetyzone.html',{'map':maps})

def showszMarker(request):
    map = folium.Map(location=[37.6511988,127.0161604],zoom_start=12)
    folium.Marker([37.566345, 126.977893],popup='testtest').add_to(map)
    #han = SafetyZone.objects.all()
    for i in range(1,101):
        han = SafetyZone.objects.get(safety_zone_pk=i)
        folium.Marker([ST_X(han.safety_loc), ST_Y(han.safety_loc)],popup='testtest').add_to(map)
    maps = map._repr_html_()
    return render(request,'safetyzone.html',{'map':maps})