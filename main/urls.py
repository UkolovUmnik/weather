"""
URL configuration for raschet_zarplati project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
import os


urlpatterns = [
    #path("pogoda_calendar/<str:gorod>/<str:radio>/update_form/<str:year>/<str:month_number>/", views.update_form_weather_calendar, {'requested_permission':'Погода календарь'}),
    path("pogoda_calendar/<str:gorod>/<str:radio>/<str:operation>/<int:id>/", views.change_weather_calendar, {'requested_permission':'Погода календарь'}),
    path("pogoda_calendar/<str:gorod>/<str:radio>/", views.page_weather_calendar, {'requested_permission':'Погода календарь'}),
    path("pogoda_calendar/<str:gorod>/", views.spisok_radio, {'requested_permission':'Погода календарь'}),
    path('pogoda_calendar/', views.spisok_gorodov, {'requested_permission':'Погода календарь'}, name='Погода календарь'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('settings/', include('settings.urls')),
    path("", views.index, name='home'),    
]
