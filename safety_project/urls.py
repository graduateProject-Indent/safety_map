"""safety_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import safety_map.views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('home/',safety_map.views.home,name='home'),
    path('',safety_map.views.startpage,name='startpage'),
    path('home/',safety_map.views.showMaps,name='showMaps'),
    path('female/',safety_map.views.showFemale,name='showFemale'),
    path('female2/',safety_map.views.pathFinder,name='pathFinder'),
    path('filter_safeyzone_bell/',safety_map.views.filter_safetyzone_bell,name = 'filter_safetyzone_bell'),
    path('mypage/',safety_map.views.mypage,name='mypage'),
    path('manage_alarm/',safety_map.views.manage_alarm,name='manage_alarm'),
    path('manage_danger_map/',safety_map.views.manage_danger_map,name='manage_danger_map'),
    path('manage_protecter/',safety_map.views.manage_protecter,name='manage_protecter'),
    path('danger_map/',safety_map.views.danger_map,name='danger_map'),
    path('register_danger/',safety_map.views.register_danger,name='register_danger'),

]
#한정원 filter_safetyzone_bell 추가