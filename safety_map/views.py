from safety_map.models import *
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import *
import random
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
import geog
import numpy as np
from shapely import *
from shapely.geometry import *
from shapely.ops import unary_union
#from shapely import wkb,wkt
#from shapely.geometry import mapping, shape, Polygon, MultiPoint,MultiPolygon,Point
from shapely.validation import explain_validity
from plpygis import Geometry
from folium.features import CustomIcon
import branca

g = geocoder.ip('me')
gu_coordinate=""
global_contain_coordinate=[]
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
    global g
    count=0
    crime_type=""
    loc_list=[]
    if request.method=="POST":
        filter_value=request.POST['female_filter']
        crime_type="전체_"+filter_value
    female_total=Female2.objects.filter(gu='도봉구',female2_crime_type=crime_type).all()
    loc_list=[]
    for loc in female_total:
        gis= Geometry(loc.female2_crime_loc.hex()[8:])
        to_geojson=convert.wkt_to_geojson(str(gis.shapely))
        to_coordinate=json.loads(to_geojson)
        contain_coordinate=shape(to_coordinate)
        crime_location={"type":"Feature","geometry":to_coordinate}
        loc_list.append(crime_location)
    pistes = {"type":"FeatureCollection","features":loc_list}
    #print(pistes)
    #style = {'fillColor': '#DC143C', 'lineColor': '#00FFFFFF'}
    map = folium.Map(location=[37.55582994870823, 126.9726320033982],zoom_start=15)
    folium.GeoJson(pistes).add_to(map)
    maps=map._repr_html_()
    return render(request, 'home.html',{'map':maps,'pistes':pistes})


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


def pathSetting(request):
    return render(request,'pathFinder.html')

def pathFinder(request):
    global global_contain_coordinate
    global gu_coordinate
    gu_list=['종로구','중구','용산구','성동구','광진구',
    '동대문구','중랑구','성북구','강북구','도봉구',
    '노원구','은평구','서대문구','마포구','양천구',
    '강서구','구로구','금천구','영등포구','동작구',
    '관악구','서초구','강남구','송파구','강동구',]
    loc_list=[]
    if request.method=="POST":
        startPoint=request.POST.get('start')
        endPoint=request.POST.get('end')
        print(startPoint,endPoint)
        for find_gu in gu_list:
            if find_gu in startPoint:
                startGu=find_gu
            else:
                pass
            if find_gu in endPoint:
                endGu=find_gu
            else:
                pass
        female_start=Female2.objects.filter(female2_crime_type="전체_전체",gu=startGu).all()
        female_end=Female2.objects.filter(female2_crime_type="전체_전체",gu=endGu).all()
        female_total=female_start.union(female_end,all=False)
        gu_start=Female2.objects.filter(female2_crime_type="위험구",gu=startGu).all()
        gu_end=Female2.objects.filter(female2_crime_type="위험구",gu=endGu).all()
        global_gu=(gu_start|gu_end)
        if len(global_gu)!=1:
            for g in global_gu:
                gu_gis= Geometry(g.female2_crime_loc.hex()[8:])
                gu_geojson=convert.wkt_to_geojson(str(gu_gis.shapely))
                gu_coords=shape(json.loads(gu_geojson))
                loc_list.append(gu_coords)
            gu_coordinate=loc_list[0].union(loc_list[1])
        else:
            global_gu=(gu_start|gu_end).get()  
            gu_gis= Geometry(global_gu.female2_crime_loc.hex()[8:])
            gu_geojson=convert.wkt_to_geojson(str(gu_gis.shapely))
            gu_coordinate=shape(json.loads(gu_geojson))
        
        for loc in female_total:
            gis= Geometry(loc.female2_crime_loc.hex()[8:])
            to_geojson=convert.wkt_to_geojson(str(gis.shapely))
            to_coordinate=json.loads(to_geojson)
            contain_coordinate=shape(to_coordinate)
            global_contain_coordinate.append(contain_coordinate)
   
    return HttpResponse(json.dumps({'reseponse':'true'}),content_type="application/json")

def containsPoint(request):
    global gu_coordinate
    pointlist=[]
    line=""
    if request.method=="POST":
        pistes=request.POST.get('draw')
        pist=pistes.split(",")
        for p in pist:
            if (pist.index(p)%2==0):
                x=p
                y=pist[pist.index(p)+1]
                point=Point(float(y),float(x))
                pointlist.append(point)
        count=0

        linear=LineString(pointlist).buffer(0.005)
        for multi in global_contain_coordinate:
            for c in pointlist:
                if multi.contains(c):
                    linear=linear.difference(multi)
        for l in list(linear):
            line+="_"+str(l.centroid.x)+","+str(l.centroid.y)
    return HttpResponse(json.dumps({'p':line[1:]}),content_type="application/json")

