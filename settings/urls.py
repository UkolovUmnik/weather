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

page_prmissions_goroda_and_directions="permissions_goroda_and_directions/"
page_permissions_for_urls="permissions_for_urls/"
urlpatterns = [
    path("lists/parameters_weather/<str:operation>/<int:id>/", views.change_parameters_weather, {'requested_permission':'Настройки/Справочники'}),
    path("lists/goroda_paramtres_weather/<str:operation>/<int:id>/", views.change_goroda_paramtres_weather, {'requested_permission':'Настройки/Справочники'}),
    path("lists/composite_weather/<str:operation>/<int:id>/", views.change_composite_weather, {'requested_permission':'Настройки/Справочники'}),
    path("lists/constant_weather/<str:operation>/<int:id>/", views.change_constant_weather, {'requested_permission':'Настройки/Справочники'}),
    path("lists/gorod_and_radio/<str:operation>/<int:id>/", views.change_gorod_and_radio, {'requested_permission':'Настройки/Справочники'}),
    path("lists/radio/<str:operation>/<int:id>/", views.change_radio, {'requested_permission':'Настройки/Справочники'}),
    path("lists/gorod/<str:operation>/<int:id>/", views.change_gorod, {'requested_permission':'Настройки/Справочники'}),

    path(page_permissions_for_urls+"create_perm_url_user/", views.create_perm_url_user, {'requested_permission':'Настройки/Резрешения на просмотр страниц'}),
    path(page_permissions_for_urls+"delete_perm_url_user/<int:id>/", views.delete_perm_url_user, {'requested_permission':'Настройки/Резрешения на просмотр страниц'}),

    path(page_permissions_for_urls+"create_perm_url_group/", views.create_perm_url_group, {'requested_permission':'Настройки/Резрешения на просмотр страниц'}),
    path(page_permissions_for_urls+"delete_perm_url_group/<int:id>/", views.delete_perm_url_group, {'requested_permission':'Настройки/Резрешения на просмотр страниц'}),
 
    path(page_prmissions_goroda_and_directions+"create/", views.create_permissions_goroda_and_directions,   {'requested_permission':'Настройки/Резрешения на города и направления'}),
    path(page_prmissions_goroda_and_directions+"edit/<int:id>/",  views.edit_permissions_goroda_and_directions, {'requested_permission':'Настройки/Резрешения на города и направления'}),
    path(page_prmissions_goroda_and_directions+"delete/<int:id>/", views.delete_permissions_goroda_and_directions,  {'requested_permission':'Настройки/Резрешения на города и направления'}),

    path(page_permissions_for_urls, views.page_permissions_for_urls, {'requested_permission':'Настройки/Резрешения на просмотр страниц'}, name='Настройки/Резрешения на просмотр страниц'), 
    path(page_prmissions_goroda_and_directions, views.page_permissions_goroda_and_directions, {'requested_permission':'Настройки/Резрешения на города и направления'},  name='Настройки/Резрешения на города и направления'),

    path("tables/", views.index, {'requested_permission':'Настройки/Таблицы_мотивации'}, name='Настройки/Таблицы_мотивации'),
    path("lists/", views.lists, {'requested_permission':'Настройки/Справочники'}, name='Настройки/Справочники'),
    path("", views.page_settings, {'requested_permission':'Настройки'}, name='Настройки')
]
