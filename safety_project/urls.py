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
from django.urls import path, include
import safety_map.views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('home/',safety_map.views.home,name='home'),
    path('',safety_map.views.startpage,name='startpage'),
    path('home/',safety_map.views.showMaps,name='showMaps'),
    path('female/',safety_map.views.showFemale,name='showFemale'),
    path('pathfinder/',safety_map.views.pathFinder,name='pathFinder'),
    path('filter_safeyzone/',safety_map.views.filter_safetyzone,name = 'filter_safetyzone'),
    path('save_mapimg/',safety_map.views.save_mapimg,name='savemapimg'),
    path('mypage/',safety_map.views.mypage,name='mypage'),
    path('manage_alarm/',safety_map.views.manage_alarm,name='manage_alarm'), #알람 관리
    path('manage_danger_map/',safety_map.views.manage_danger_map,name='manage_danger_map'), #위험물 관리(수정,삭제)
    path('manage_protecter/',safety_map.views.manage_protecter,name='manage_protecter'), #보호자 관리
    path('danger_map/',safety_map.views.danger_map,name='danger_map'), #전체 위험물 보기
    path('register_danger/',safety_map.views.register_danger,name='register_danger'), #위험물등록하기 폼이 보여짐
    path('register_danger_done/',safety_map.views.register_danger_done,name='register_danger_done'), #위험물등록하기 제출?
    path('<int:danger_id>/',safety_map.views.detail_danger,name='detail_danger'), #위험물 상세보기
]