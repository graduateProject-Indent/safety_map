from django.shortcuts import render
import folium
import urllib.request
import datetime
import time
import json
import webbrowser
from safety_map.models import DongLevel
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

def mypage(request):
    return render(request, 'mypage.html')

def donglevel(request):
    map = folium.Map(location=[37.6511988,127.0161604],zoom_start=12)

    m = DongLevel.objects.all()
    for i in m:
        gis= Geometry(i.dong_loc.hex()[8:])

        folium.Choropleth(geo_data=gis,
                      data = i.dong_level_tot,
                      fill_color="BuPu",
                      columns=('동','위험등급'),
                      key_on=i.dong_loc,
                      legend_name="위험등급",
                      ).add_to(map)
    maps=map._repr_html_() 
    return render(request, 'dong.html', {'map':maps})