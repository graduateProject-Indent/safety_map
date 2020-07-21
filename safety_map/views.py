from django.shortcuts import render,get_object_or_404,redirect
import folium
import urllib.request
import datetime
import time
import json
import webbrowser
from .forms import DangerForm
from .models import Danger

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