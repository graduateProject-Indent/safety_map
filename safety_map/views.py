from django.shortcuts import render,get_object_or_404
from safety_map.models import *
import folium
import binascii
import urllib.request
import datetime
import time
import json
import webbrowser
import geocoder
import geodaisy.converters as convert
from shapely import wkb
from shapely.geometry import mapping, shape, Polygon, MultiPoint
from plpygis import Geometry
from folium.features import CustomIcon



# Create your views here.
def home(request):
    return render(request, 'home.html')

def startpage(request):
    return render(request, 'startpage.html')

def showMaps(request):
    g = geocoder.ip('me')
    map = folium.Map(location=g.latlng,zoom_start=15)
    maps=map._repr_html_() 
    return render(request, 'home.html',{'map':maps})

def showFemale(request):
    crime_type=""
    if request.method=="POST":
        filter_value=request.POST['female_filter']
        crime_type="전체_"+filter_value
    female_total=Female2.objects.filter(female2_crime_type=crime_type).all()
    loc_list=[]
    for loc in female_total:
        gis= Geometry(loc.female2_crime_loc.hex()[8:])
        to_geojson=convert.wkt_to_geojson(str(gis.shapely))
        to_coordinate=json.loads(to_geojson)
        crime_location={"type":"Feature","geometry":to_coordinate}
        loc_list.append(crime_location)
    pistes = {"type":"FeatureCollection","features":loc_list}
    #print(pistes)
    map = folium.Map(location=[37.55582994870823, 126.9726320033982],zoom_start=18)
    folium.GeoJson(pistes, name='json_data').add_to(map)
    maps=map._repr_html_()

    return render(request, 'home.html',{'map':maps})

#한정원 : 안심장소
def filter_safetyzone(request): # 한정원
    safety_type = ""
    if request.method=="POST":
        filter_value=request.POST['safetyZone_filter']
        safety_type=filter_value
    safetyzone_ob_all = SafetyZone.objects.filter(safety_type=safety_type).all()
    map = folium.Map(location=[37.55582994870823, 126.9726320033982],zoom_start=12)
    
    for loc in safetyzone_ob_all:
        gis = Geometry(loc.safety_loc.hex()[8:])
        to_geojson=convert.wkt_to_geojson(str(gis.shapely))
        to_coordinate=json.loads(to_geojson)
        #print(to_coordinate)
        folium.Marker([to_coordinate['coordinates'][0],to_coordinate['coordinates'][1]],popup='hello').add_to(map)
    maps=map._repr_html_()
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

