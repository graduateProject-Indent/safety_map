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
    if request.method=="POST":
        filter_value=request.POST['female_filter']
        crime_type="전체_"+filter_value
    female_total=Female2.objects.filter(female2_crime_type=crime_type).all()
    loc_list=[]
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
    style = {'fillColor': '#DC143C', 'lineColor': '#00FFFFFF'}
    map = folium.Map(location=mid,zoom_start=15)
    folium.GeoJson(pistes,style_function=lambda x: style).add_to(map)
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
