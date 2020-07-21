from django.shortcuts import render,get_object_or_404
from .models import *
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
from plpygis import Geometry


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
    female_total=Female2.objects.filter(female2_crime_type="전체_전체").all()
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
    return render(request, 'female.html',{'map':maps})