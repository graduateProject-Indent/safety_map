from safety_map.models import *
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import *
from .Astar import * 
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
from shapely.validation import explain_validity
from plpygis import Geometry
from folium.features import CustomIcon
from PIL import ImageGrab # pip install pillow
import pandas as pd # pip install pandas
from django.db import models
from django.http import HttpResponse
from pprint import pprint
from geomet import wkb
from django.http import HttpResponseRedirect
from django.shortcuts import render
import branca.colormap as cmp
import math
import hexgrid # han : pip install hexgrid-py
import morton 
import configparser
from geomet import wkb
import urllib
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
config = configparser.ConfigParser()
config.read('database.ini')
g = geocoder.ip('me')
startGu=""
endGu=""
getGu=""
startX=""
startY=""
endX=""
endY=""

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
    global getGu
    crime_type=""
    loc_list=[]
    if request.method=="POST":
        filter_value=request.POST['female_filter']
        crime_type="전체_"+filter_value
    female_total=Female2.objects.filter(gu=getGu,female2_crime_type=crime_type).all()

    linear = cmp.LinearColormap(
    [ 'green','blue','red'],
    vmin=10, vmax=300)

    map = folium.Map(location=[37.55582994870823, 126.9726320033982],zoom_start=15)
    for loc in female_total:
        gis= Geometry(loc.female2_crime_loc.hex()[8:])
        contain_coordinate=shape(gis.geojson)
        crime_location={"type":"Feature","properties":{'area':math.ceil(round(contain_coordinate.length,5)*100000)},"geometry":gis.geojson}
        folium.GeoJson(crime_location,style_function=lambda feature: {
            'fillColor': linear(feature['properties']['area']),
            'color': linear(feature['properties']['area']),     
            'weight': 1  
        }).add_to(map)
        linear.add_to(map)
    
    
    maps=map._repr_html_()
    return render(request, 'home.html',{'map':maps})


def filter_safetyzone(request): #안심장소보기
    global getGu
    safety_type = ""
    gu_type = ""
    mkurl = ""
    map = folium.Map(location=[37.55582994870823, 126.9726320033982],zoom_start=12)

    if request.method=="POST":
        filter_value=request.POST['safetyZone_filter']
        safety_type=filter_value

    # 편의점을 선택한 경우 선택된 구를 출력
    if(safety_type=="편의점") : 
        mkurl = "safety_map/static/img/mk_cvs.png" #편의점 마커 이미지
        safetyzone_ob_all = SafetyZone.objects.filter(gu=getGu) # 구 입력 방식 정해지면 '종로구'자리에 gu_type 넣으면 된다.

    # 경찰서, 지구대, 파출소를 선택한 경우 서울 전체
    else : 
        if(safety_type=="경찰서"):
            mkurl = "safety_map/static/img/mk_police_station.png" # 경찰서 마커 이미지
        elif(safety_type=="지구대"):
            mkurl = "safety_map/static/img/mk_police_unit.png" # 지구대 마커 이미지
        elif(safety_type=="파출소"):
            mkurl = "safety_map/static/img/mk_police_box.png" # 파출소 마커 이미지
        safetyzone_ob_all = SafetyZone.objects.filter(safety_type=safety_type).all()

    # 마커 지도에 추가
    for loc in safetyzone_ob_all:
        icon = folium.features.CustomIcon(icon_image=mkurl,icon_size=(50,50))
        gis = Geometry(loc.safety_loc.hex()[8:])
        to_geojson=convert.wkt_to_geojson(str(gis.shapely))
        to_coordinate=json.loads(to_geojson)
        marker = folium.map.Marker([to_coordinate['coordinates'][0],to_coordinate['coordinates'][1]],icon=icon)
        marker.add_to(map)

    maps=map._repr_html_()
    return render(request,'home.html',{'map':maps})

def save_mapimg(request):
    import time # 맨 위에 import 있는데 지우면 에러가 나는 행
    map = folium.Map(location=[37.55582994870823, 126.9726320033982],zoom_start=12)
    now  = time.localtime()
    time = "%04d-%02d-%02d-%02dh-%02dm-%02ds" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    img = ImageGrab.grab()
    # 캡쳐한 지도 사진 저장 위치
    saveas = "{}{}".format("safety_map/static/save_mapimg/safetymap"+time,'.png')
    img.save(saveas)
    maps=map._repr_html_()
    return render(request,'home.html',{'map':maps})


def mypage(request):
    return render(request, 'mypage.html')

def showKid(request): #아동필터
    global g
    global getGu
    accident_type = ""
    loc_list = []

    if request.method == 'POST':
        filter_value = request.POST["kid_filter"]
        accident_type = filter_value
        
    # 어린이 보행사고를 클릭한 경우    
    if filter_value == "스쿨존사고":
        accident_type = filter_value+"다발지역"
    elif filter_value == "어린이보행사고":
        accident_type =filter_value
    else:
        accident_type = filter_value
        
    kid_accident = Kid.objects.filter(gu=getGu, kid_accident_type = accident_type).all()

    #colormap_dept = cmp.StepColormap(colors=['#00ae53', '#86dc76', '#daf8aa','#ffe6a4', '#ff9a61', '#ee0028'], 
    #                                vmin=10, vmax=310)
                                    
    for i in kid_accident:
        gis = Geometry(i.kid_accident_loc.hex()[8:])
        to_geojson = convert.wkt_to_geojson(str(gis.shapely))
        to_coordinate = json.loads(to_geojson)
        contain_coordinate=shape(to_coordinate)
        crime_location = {"type":"Feature","geometry":to_coordinate}
        loc_list.append(crime_location)
    pistes = {"type":"FeatureCollection","features":loc_list}

    map = folium.Map(location=[37.55582994870823, 126.9726320033982],zoom_start=15)

    folium.GeoJson(pistes).add_to(map)
    
    maps=map._repr_html_()
    return render(request, 'home.html',{'map':maps,'pistes':pistes})
    #return render(request, 'home.html',{'map':maps})
   


def donglevel(request):
    map = folium.Map(location=[37.5518838,126.9858763],zoom_start=12)
    dongm = DongLevel.objects.values('dong_level_tot','dong_nm')
    dong_df = pd.DataFrame(dongm)
    dongloc = DongLevel.objects.all()
    loc_list=[]
    for i in dongloc:
        gis= Geometry(i.dong_loc.hex()[8:])  
        crime_location = {"type":"Feature","properties":{"dong_nm":i.dong_nm},"geometry":gis.geojson}
        loc_list.append(crime_location)
    pistes = {"type":"FeatureCollection","features":loc_list}
    
    folium.Choropleth(geo_data=pistes, data = dong_df,
                    columns=('dong_nm','dong_level_tot'),
                    fill_color='BuPu',
                    key_on='feature.properties.dong_nm'
                    ).add_to(map)

    maps=map._repr_html_() 
    return render(request, 'home.html', {'map':maps})

def manage_alarm(request):
    return render(request, 'manage_alarm.html')

def manage_danger_map(request):
    return render(request, 'manage_danger_map.html')

def manage_protecter(request):
    return render(request, 'manage_protecter.html')






def danger_map(request): # 한 : [미완성]위험물 지도를 보여줌(안심장소와 비슷하게 마커 띄우기)
    map = folium.Map(location=[37.55582994870823, 126.9726320033982],zoom_start=12)
    dangers = Danger.objects
    dangers = map._repr_html_()
    return render(request, 'danger_map.html', {'dangers':dangers})

def register_danger(request): # han : [수정요구]
    g = geocoder.ip('me') # han : [!]현재위치
    danger_loc = g.latlng

    if request.method == "POST":
        post_danger_type = request.POST['danger_type']
        post_danger_img = request.FILES.get('danger_img',False)
        point_danger_loc={"type":"Point","coordinates":danger_loc}

        model_test_instance = Danger(danger_type = post_danger_type, danger_img = post_danger_img,
                                     danger_loc=wkb.dumps(point_danger_loc)) # han [!] auth_user_id_fk가 필요해요
        model_test_instance.save()
        

        return render(request,'danger_map.html') # han : 위험물 등록이 성공하면 danger_map.html
        
    else:
        return render(request, 'register_danger.html', {'g':g.latlng})
    
        #pass
        
    return render(request, 'register_danger.html', {'g':g.latlng})
    

def detail_danger(request, danger_id):
    danger_detail = get_object_or_404(Danger, pk=danger_id)
    return render(request, 'detail_danger.html',{'danger':danger_detail})


def pathSetting(request):
    map = folium.Map(location=g.latlng,zoom_start=15)
    maps=map._repr_html_() 
    api_key=config['DATABASE']['APPKEY']
    return render(request,'pathFinder.html',{'map':maps,'api_key':api_key})

def pathFinder(request): #위험지역 받는 함수
    global startX,startY,endX,endY,startGu,endGu
    gu_list=['종로구','중구','용산구','성동구','광진구',
    '동대문구','중랑구','성북구','강북구','도봉구',
    '노원구','은평구','서대문구','마포구','양천구',
    '강서구','구로구','금천구','영등포구','동작구',
    '관악구','서초구','강남구','송파구','강동구',]
    loc_list=[]
    if request.method=="POST":
        startPoint=request.POST.get('start')
        endPoint=request.POST.get('end')
        startX=request.POST.get('startX')
        startY=request.POST.get('startY')
        endX=request.POST.get('endX')
        endY=request.POST.get('endY')
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
        for loc in female_total:
            gis= Geometry(loc.female2_crime_loc.hex()[8:])
            contain_coordinate=shape(gis.geojson)
            crime_location={"type":"Feature","geometry":gis.geojson}
            loc_list.append(crime_location)
    pistes = {"type":"FeatureCollection","features":loc_list}
    return HttpResponse(json.dumps({'result':pistes}),content_type="application/json")

def normalPath(request):
    global gu_coordinate,startX,startY,endX,endY
    pointlist=[]
    polyline=[]
    line=""
    count=0
    if request.method=="POST":
        pistes=request.POST.get('draw')
        pist=pistes.split(",")
        for p in pist:
            if (pist.index(p)%2==0):
                x=p
                y=pist[pist.index(p)+1]
                point=[float(y),float(x)]
                pointlist.append(point)

        
    crime_location={"type":"Feature","geometry":{"type":"LineString","coordinates":pointlist}}
  
    pistes = {"type":"FeatureCollection","features":[crime_location]}
    return HttpResponse(json.dumps({'pistes':pistes}),content_type="application/json")

def getGu(request):
    global getGu
    if request.method=='POST':
        getGu=request.POST.get('gu')
    return HttpResponse(json.dumps({'result':'true'}),content_type="application/json")
        
        

def aStar(request):
    global startGu,endGu
    center=hexgrid.Point((float(startX)+float(endX))/2,(float(startY)+float(endY))/2)
    rate = 110.574 / (111.320 * math.cos(37.55582994870823 * math.pi / 180))
    grid = hexgrid.Grid(hexgrid.OrientationFlat, center, Point(rate*0.00015,0.00015), morton.Morton(2, 32))
    sPoint=grid.hex_at(Point(float(startX),float(startY)))
    ePoint=grid.hex_at(Point(float(endX),float(endY)))
    map_size=max(abs(sPoint.q),abs(sPoint.r))
    road1=Roadtohexgrid.objects.filter(is_danger=1,hexgrid_gu=startGu).all()
    road2=Roadtohexgrid.objects.filter(is_danger=1,hexgrid_gu=endGu).all()
    total_road=road1.union(road2,all=False)
    wall1=Roadtohexgrid.objects.filter(is_danger=0,hexgrid_gu=startGu).all()
    wall2=Roadtohexgrid.objects.filter(is_danger=0,hexgrid_gu=endGu).all()
    total_wall=wall1.union(wall2,all=False)
    wh=GridWithWeights(layout_flat,Point(rate*0.00015,0.00015),center,map_size+5)
    for r in total_road:
        gis= Geometry(r.hexgrid_loc.hex()[8:])
        h=grid.hex_at(shape(gis.geojson))
        wh.weights[(h.q,h.r)]=1
    
    for w in total_wall:
        gis= Geometry(w.hexgrid_loc.hex()[8:])
        h=grid.hex_at(shape(gis.geojson))
        wh.weights[(h.q,h.r)]=200
    
    start, goal = (sPoint.q,sPoint.r), (ePoint.q,ePoint.r)
    came_from, cost_so_far = a_star_search(wh, start, goal)
    pointList=reconstruct_path(came_from, start=start, goal=goal)
    plist=[]
    for p in pointList:
        point=wh.hex_to_pixel(hexgrid.Hex(p[0],p[1]))
        plist.append([point.x,point.y])
    crime_location={"type":"Feature","geometry":{"type":"LineString","coordinates":plist}}
    pistes = {"type":"FeatureCollection","features":[crime_location]}
    
    return HttpResponse(json.dumps({'pistes':pistes}),content_type="application/json")


def logout(request):
    auth.logout(request)
    return render(request, 'startpage.html') 
