from django.shortcuts import render,get_object_or_404
from safety_map.models import *
from django.shortcuts import render,get_object_or_404,redirect
from .models import *
import folium
import binascii
import urllib.request
import datetime
import time
import json
import webbrowser
from .forms import DangerForm
from .models import Danger
import geocoder
import geojson
import geodaisy.converters as convert
from shapely import wkb,wkt
from shapely.geometry import mapping, shape, Polygon, MultiPoint,MultiPolygon
from plpygis import Geometry
from folium.features import CustomIcon
import branca

g = geocoder.ip('me')
mid=g.latlng
top_left=[mid[1]-0.008,mid[0]+0.008]
bottom_left=[mid[1]+0.008,mid[0]+0.008]
bottom_right=[mid[1]+0.008,mid[0]-0.008]
top_right=[mid[1]-0.008,mid[0]-0.008]
polyNY_shapely = Polygon([(top_left), (bottom_left), (bottom_right), (top_right)])

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
    global mid
    global polyNY_shapely
    crime_type=""
    loc_list=[]
    if request.method=="POST":
        filter_value=request.POST['female_filter']
        crime_type="전체_"+filter_value
        female_total=Female2.objects.filter(female2_crime_type=crime_type).all()
        
        for loc in female_total:
            gis= Geometry(loc.female2_crime_loc.hex()[8:])
            to_geojson=convert.wkt_to_geojson(str(gis.shapely))
            to_coordinate=json.loads(to_geojson)
            contain_coordinate=shape(to_coordinate)
            if polyNY_shapely.contains(contain_coordinate):
                crime_location={"type":"Feature","geometry":to_coordinate}
                loc_list.append(crime_location)
        
    pistes = {"type":"FeatureCollection","features":loc_list}
    #print(pistes)
    
    map = folium.Map(location=mid,zoom_start=15)
    folium.GeoJson(pistes).add_to(map)
    maps=map._repr_html_()

    return render(request, 'home.html',{'map':maps})

def filter_safetyzone(request): #안심장소보기
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
    dangers = Danger.objects
    return render(request, 'danger_map.html', {'dangers':dangers})

def register_danger(request):
    if request.method == "POST":
        form = DangerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danger_map')
    else:
        form = DangerForm()
    return render(request, 'register_danger.html', {'form':form})

def detail_danger(request, danger_id):
    danger_detail = get_object_or_404(Danger, pk=danger_id)
    return render(request, 'detail_danger.html',{'danger':danger_detail})
