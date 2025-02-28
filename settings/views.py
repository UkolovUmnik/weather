import os
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from settings.models import goroda,radio,permissions_goroda_and_directions
from settings.models import permissions_for_urls_groups,permissions_for_urls_users,names_sections_and_urls,goroda_and_radio,constant_weather,composite_weather,goroda_paramtres_weather,parameters_weather

path_to_segments_weather_radio=os.path.abspath(os.curdir)+'\\files\segments_weather\Радио'
path_to_segments_weather_goroda=os.path.abspath(os.curdir)+'\\files\segments_weather\Города'

def check_permission_for_url(user,requested_permission):
    status=False
    list_permissions=[]
    if user.is_superuser:
        status=True
    else:
        username = user.username
        user_groups=user.groups.all() #получаю список групп
        #заполняем список разрешений разрешениями группы (имена ссылок)
        for element in user_groups: 
            permissions_for_group=permissions_for_urls_groups.objects.filter(name_group=element.name)
            for permission in permissions_for_group:
                list_permissions.append(permission.name_url)
        #заполняем список разрешений разрешениями пользователя (имена ссылок)
        permissions_for_user=permissions_for_urls_users.objects.filter(name_user=username)
        for permission in permissions_for_user:
            list_permissions.append(permission.name_url)
        #нюанс, что права в списке могут дублироваться (у группы и у пользователя может быть один и тот же доступ указан)
        for permission in list_permissions:
            if permission==requested_permission:
                status=True
                break
            
    return status


# получение данных из бд
@login_required
def index(request, requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        table_goroda=goroda.objects.all()
        return render(request, "settings/tables.html", {"table_goroda":table_goroda})
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")


@login_required
def page_settings(request, requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        return render(request, "settings/page_settings.html")
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")

@login_required
def lists(request,requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        table_goroda=goroda.objects.all()
        table_radio=radio.objects.all()
        table_goroda_and_radio=goroda_and_radio.objects.all()
        table_constant_weather=constant_weather.objects.all()
        table_composite_weather=composite_weather.objects.all()
        table_parameters_weather=parameters_weather.objects.all()
        table_goroda_paramtres_weather=goroda_paramtres_weather.objects.all()
        return render(request, "settings/lists.html",{"table_goroda":table_goroda,"table_radio":table_radio,
                                                      'table_goroda_and_radio':table_goroda_and_radio,'table_constant_weather':table_constant_weather,
                                                      'table_composite_weather':table_composite_weather,'table_goroda_paramtres_weather':table_goroda_paramtres_weather,
                                                      'table_parameters_weather':table_parameters_weather
                                                      })
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")


@login_required
def page_permissions_goroda_and_directions(request,requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        tabel_permissions_goroda_and_directions=permissions_goroda_and_directions.objects.all()
        return render(request, "settings/premissions_goroda_and_directions.html",{"tabel_permissions_goroda_and_directions":tabel_permissions_goroda_and_directions})
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
        
@login_required
def page_permissions_for_urls(request,requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        table_permissions_for_urls_users=permissions_for_urls_users.objects.all()
        tabel_names_sections_and_urls=names_sections_and_urls.objects.all()
        tabel_permissions_for_urls_groups=permissions_for_urls_groups.objects.all()
        return render(request, "settings/permissions_for_urls.html",{"table_permissions_for_urls_users":table_permissions_for_urls_users,
                                                                     "tabel_names_sections_and_urls":tabel_names_sections_and_urls,
                                                                     "tabel_permissions_for_urls_groups":tabel_permissions_for_urls_groups})
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")

@login_required
def create_permissions_goroda_and_directions(request,requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        try:
            if request.method == "POST":
                data = permissions_goroda_and_directions()
                data.name=request.POST.get("name")
                data.gorod = request.POST.get("gorod")
                data.direction = request.POST.get("direction")
                data.save()
                return HttpResponseRedirect("/settings/permissions_goroda_and_directions/")
            else:
                users = User.objects.all()
                table_goroda=goroda.objects.all()
                table_directions=directions.objects.all()
                return render(request, "settings/create_permission_gorod_and_direction.html",{"table_goroda":table_goroda,"table_directions":table_directions,"users":users})
        except permissions_goroda_and_directions.DoesNotExist:
            return HttpResponseNotFound("<h2>Данные не найдены</h2>")
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")

# изменение данных в бд
@login_required
def edit_permissions_goroda_and_directions(request, id ,requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        try:
            data = permissions_goroda_and_directions.objects.get(id=id)
            if request.method == "POST":
                data.name=request.POST.get("name")
                data.gorod = request.POST.get("gorod")
                data.direction = request.POST.get("direction")
                data.save()
                return HttpResponseRedirect("/settings/permissions_goroda_and_directions/")
            else:
                users = User.objects.all()
                table_goroda=goroda.objects.all()
                table_directions=directions.objects.all()
                return render(request, "settings/edit_permission_gorod_and_direction.html", {"data": data,"table_goroda":table_goroda,"table_directions":table_directions,"users":users})
        except permissions_goroda_and_directions.DoesNotExist:
            return HttpResponseNotFound("<h2>Данные не найдены</h2>")
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
     
# удаление данных из бд
@login_required
def delete_permissions_goroda_and_directions(request, id ,requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        try:
            data = permissions_goroda_and_directions.objects.get(id=id)
            data.delete()
            return HttpResponseRedirect("/settings/permissions_goroda_and_directions/")
        except permissions_goroda_and_directions.DoesNotExist:
            return HttpResponseNotFound("<h2>Данные не найдены</h2>")
    else:
       return HttpResponseNotFound("<h2>Доступ запрещен</h2>")   

@login_required
def create_perm_url_user(request, requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        try:
            if request.method == "POST":
                data = permissions_for_urls_users()
                data.name_user = request.POST.get("name_user")
                data.name_url = request.POST.get("name_url")
                data.save()
                return HttpResponseRedirect("/settings/permissions_for_urls/")             
            else:
                users = User.objects.all()
                table_sections_and_urls=names_sections_and_urls.objects.all()       
                return render(request, "settings/create_perm_url_user.html",{"users": users,"table_sections_and_urls":table_sections_and_urls})
                
        except permissions_for_urls_users.DoesNotExist:
            return HttpResponseNotFound("<h2>Данные не найдены</h2>")
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")

@login_required
def delete_perm_url_user(request, id, requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        try:
            data = permissions_for_urls_users.objects.get(id=id)
            data.delete()
            return HttpResponseRedirect("/settings/permissions_for_urls/")
        except permissions_for_urls_users.DoesNotExist:
            return HttpResponseNotFound("<h2>Данные не найдены</h2>")
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>") 

@login_required
def create_perm_url_group(request, requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        try:
            if request.method == "POST":
                data = permissions_for_urls_groups()
                data.name_group = request.POST.get("name_group")
                data.name_url = request.POST.get("name_url")
                data.save()
                return HttpResponseRedirect("/settings/permissions_for_urls/")             
            else:
                groups=Group.objects.all()
                table_sections_and_urls=names_sections_and_urls.objects.all()       
                return render(request, "settings/create_perm_url_group.html",{"groups": groups,"table_sections_and_urls":table_sections_and_urls})
                
        except permissions_for_urls_groups.DoesNotExist:
            return HttpResponseNotFound("<h2>Данные не найдены</h2>")
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>") 

     
# удаление данных из бд
@login_required
def delete_perm_url_group(request, id, requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        try:
            data = permissions_for_urls_groups.objects.get(id=id)
            data.delete()
            return HttpResponseRedirect("/settings/permissions_for_urls/")
        except permissions_for_urls_groups.DoesNotExist:
            return HttpResponseNotFound("<h2>Данные не найдены</h2>")
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")


@login_required
def change_radio(request, requested_permission, id, operation):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==False:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
    else:
        if operation=='create':
            try:
                if request.method == "POST":
                    data = radio()
                    new_radio=request.POST.get("radio")
                    data.radio = new_radio
                    data.radio_on_station=request.POST.get("radio_on_station")
                    data.save()
                    #создаем папку в файлах погоды по новое радио
                    try:
                        os.mkdir(path_to_segments_weather_radio+'\\'+new_radio)
                    except:
                        pass
                    
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    return render(request, "settings/radio.html")
            except radio.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")    
        elif operation=='edit': 
            try:
                data = radio.objects.get(id=id)
                if request.method == "POST":
                    old_radio=request.POST.get("old_radio")
                    new_radio=request.POST.get("radio")
                    data.radio = new_radio
                    data.radio_on_station=request.POST.get("radio_on_station")
                    data.save()

                    #замена значения радио в других таблицах
                    table_goroda_and_radio=goroda_and_radio.objects.filter(radio=old_radio).update(radio=new_radio)   
                    table_constant_weather=constant_weather.objects.filter(radio=old_radio).update(radio=new_radio)

                    
                    #при изменении названия радио меняем название папки в файлах погоды
                    os.rename(path_to_segments_weather_radio+'\\'+old_radio,path_to_segments_weather_radio+'\\'+new_radio)
                    
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    return render(request, "settings/radio.html", {"data": data})
            except radio.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")                
        elif operation=='delete':
            try:
                data = radio.objects.get(id=id)
                old_radio=data.radio
                data.delete()

                #замена значения радио в других таблицах
                table_goroda_and_radio=goroda_and_radio.objects.filter(radio=old_radio).delete()   
                table_constant_weather=constant_weather.objects.filter(radio=old_radio).delete()

                
                return HttpResponseRedirect("/settings/lists/")
            except radio.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")
            

@login_required
def change_gorod(request, requested_permission, id, operation):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==False:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
    else:
        if operation=='create':
            try:
                if request.method == "POST":
                    data = goroda()
                    new_gorod=request.POST.get("gorod")
                    data.gorod = new_gorod
                    data.gorod_in_yandex_weather = request.POST.get("gorod_in_yandex_weather")
                    data.gorod_on_station = request.POST.get("gorod_on_station")
                    data.gorod_id_yandex_weather = request.POST.get("gorod_id_yandex_weather")
                    data.gorod_lat_and_lon = request.POST.get("gorod_lat_and_lon")
                    data.save()

                    #создаем папку в файлах погоды по новый город
                    try:
                        os.mkdir(path_to_segments_weather_goroda+'\\'+new_gorod)
                    except:
                        pass
                    
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    return render(request, "settings/gorod.html")
            except goroda.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")    
        elif operation=='edit': 
            try:
                data = goroda.objects.get(id=id)
                if request.method == "POST":
                    old_gorod=request.POST.get("old_gorod")
                    new_gorod = request.POST.get("gorod")
                    data.gorod = new_gorod
                    data.gorod_in_yandex_weather = request.POST.get("gorod_in_yandex_weather")
                    data.gorod_on_station = request.POST.get("gorod_on_station")
                    data.gorod_id_yandex_weather = request.POST.get("gorod_id_yandex_weather")
                    data.gorod_lat_and_lon = request.POST.get("gorod_lat_and_lon")
                    data.save()

                    #замена значения города в других таблицах
                    table_goroda_and_radio=goroda_and_radio.objects.filter(gorod=old_gorod).update(gorod=new_gorod)   
                    table_constant_weather=constant_weather.objects.filter(gorod=old_gorod).update(gorod=new_gorod)

                    #при изменении названия города меняем название папки в файлах погоды
                    os.rename(path_to_segments_weather_goroda+'\\'+old_gorod,path_to_segments_weather_goroda+'\\'+new_gorod)
                    
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    return render(request, "settings/gorod.html", {"data": data})
            except goroda.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")                
        elif operation=='delete':
            try:
                data = goroda.objects.get(id=id)
                old_gorod=data.gorod
                data.delete()

                #удаление строк в других таблицах, где был город, который удаляем
                table_goroda_and_radio=goroda_and_radio.objects.filter(gorod=old_gorod).delete()   
                table_constant_weather=constant_weather.objects.filter(gorod=old_gorod).delete()
                return HttpResponseRedirect("/settings/lists/")
            except goroda.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")

@login_required
def change_gorod_and_radio(request, requested_permission, id, operation):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==False:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
    else:
        if operation=='create':
            try:
                if request.method == "POST":
                    data = goroda_and_radio()
                    data.gorod = request.POST.get("gorod")
                    data.radio = request.POST.get("radio")
                    data.save()
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    table_goroda=goroda.objects.all()
                    table_radio=radio.objects.all()
                    return render(request, "settings/gorod and radio.html", {'table_goroda':table_goroda,'table_radio':table_radio})
            except goroda_and_radio.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")    
        elif operation=='edit': 
            try:
                data = goroda_and_radio.objects.get(id=id)
                if request.method == "POST":
                    data.gorod = request.POST.get("gorod")
                    data.radio = request.POST.get("radio")
                    data.save()
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    table_goroda=goroda.objects.all()
                    table_radio=radio.objects.all()
                    return render(request, "settings/gorod and radio.html", {"data": data,'table_goroda':table_goroda,'table_radio':table_radio})
            except goroda_and_radio.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")                
        elif operation=='delete':
            try:
                data = goroda_and_radio.objects.get(id=id)
                data.delete()
                return HttpResponseRedirect("/settings/lists/")
            except goroda_and_radio.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")


@login_required
def change_constant_weather(request, requested_permission, id, operation):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==False:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
    else:
        if operation=='create':
            try:
                if request.method == "POST":
                    data = constant_weather()
                    data.gorod = request.POST.get("gorod")
                    data.radio = request.POST.get("radio")
                    data.save()
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    table_goroda=goroda.objects.all()
                    table_radio=radio.objects.all()
                    return render(request, "settings/gorod and radio.html", {'table_goroda':table_goroda,'table_radio':table_radio})
            except constant_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")    
        elif operation=='edit': 
            try:
                data = constant_weather.objects.get(id=id)
                if request.method == "POST":
                    data.gorod = request.POST.get("gorod")
                    data.radio = request.POST.get("radio")
                    data.save()
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    return render(request, "settings/gorod and radio.html", {"data": data})
            except constant_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")                
        elif operation=='delete':
            try:
                data = constant_weather.objects.get(id=id)
                data.delete()
                return HttpResponseRedirect("/settings/lists/")
            except constant_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")

@login_required
def change_composite_weather(request, requested_permission, id, operation):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==False:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
    else:
        if operation=='create':
            try:
                if request.method == "POST":
                    data = composite_weather()
                    data.gorod = request.POST.get("gorod")
                    data.radio=request.POST.get("radio")
                    table_goroda=goroda.objects.all()
                    table_parameters_weather=parameters_weather.objects.all()
                    list_goroda_additionally=''
                    for element in table_goroda:
                        gorod_status=request.POST.get(element.gorod)
                        if gorod_status=='on':
                            list_goroda_additionally+=element.gorod+','
                    list_goroda_additionally=list_goroda_additionally[:-1]
                    data.list_goroda_additionally = list_goroda_additionally
                    data.save()                   
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    table_goroda=goroda.objects.all()
                    table_radio=radio.objects.all()
                    return render(request, "settings/composite_weather.html", {'table_goroda':table_goroda,'table_radio':table_radio})
            except composite_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")    
        elif operation=='edit': 
            try:
                data = composite_weather.objects.get(id=id)
                if request.method == "POST":
                    data.gorod = request.POST.get("gorod")
                    data.radio=request.POST.get("radio")
                    table_goroda=goroda.objects.all()
                    table_parameters_weather=parameters_weather.objects.all()
                    list_goroda_additionally=''
                    for element in table_goroda:
                        gorod_status=request.POST.get(element.gorod)
                        if gorod_status=='on':
                            list_goroda_additionally+=element.gorod+','
                    list_goroda_additionally=list_goroda_additionally[:-1]
                    data.list_goroda_additionally = list_goroda_additionally
                    data.save()
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    table_goroda=goroda.objects.all()
                    table_radio=radio.objects.all()
                    list_goroda_additionally=data.list_goroda_additionally.split(',')
                    return render(request, "settings/composite_weather.html", {"data": data,'table_goroda':table_goroda,'table_radio':table_radio,'list_goroda_additionally':list_goroda_additionally})
            except composite_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")                
        elif operation=='delete':
            try:
                data = composite_weather.objects.get(id=id)
                data.delete()
                return HttpResponseRedirect("/settings/lists/")
            except composite_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")

@login_required
def change_goroda_paramtres_weather(request, requested_permission, id, operation):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==False:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
    else:
        if operation=='create':
            try:
                if request.method == "POST":
                    data = goroda_paramtres_weather()
                    data.gorod = request.POST.get("gorod")
                    table_parameters_weather=parameters_weather.objects.all()
                    list_parameters=''
                    for element in table_parameters_weather:
                        parametr_status=request.POST.get(element.parameter_weather)
                        if parametr_status=='on':
                            list_parameters+=element.parameter_weather+','
                    list_parameters=list_parameters[:-1]
                    data.list_parametres_weather = list_parameters
                    data.save()
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    table_goroda=goroda.objects.all()
                    table_parameters_weather=parameters_weather.objects.all()
                    return render(request, "settings/goroda_paramtres_weather.html", {'table_goroda':table_goroda,'table_parameters_weather':table_parameters_weather})
            except goroda_paramtres_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")    
        elif operation=='edit': 
            try:
                data = goroda_paramtres_weather.objects.get(id=id)
                if request.method == "POST":
                    data.gorod = request.POST.get("gorod")
                    table_parameters_weather=parameters_weather.objects.all()
                    list_parameters=''
                    for element in table_parameters_weather:
                        parametr_status=request.POST.get(element.parameter_weather)
                        if parametr_status=='on':
                            list_parameters+=element.parameter_weather+','
                    list_parameters=list_parameters[:-1]
                    data.list_parametres_weather = list_parameters
                    data.save()
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    table_goroda=goroda.objects.all()
                    list_parameters=data.list_parametres_weather.split(',')
                    table_parameters_weather=parameters_weather.objects.all()
                    return render(request, "settings/goroda_paramtres_weather.html", {"data": data,'table_goroda':table_goroda,'list_parameters':list_parameters,'table_parameters_weather':table_parameters_weather})
            except goroda_paramtres_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")                
        elif operation=='delete':
            try:
                data = goroda_paramtres_weather.objects.get(id=id)
                data.delete()
                return HttpResponseRedirect("/settings/lists/")
            except goroda_paramtres_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")

@login_required
def change_parameters_weather(request, requested_permission, id, operation):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==False:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
    else:
        if operation=='create':
            try:
                if request.method == "POST":
                    data = parameters_weather()
                    data.parameter_weather = request.POST.get("parameter_weather")
                    data.save()
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    return render(request, "settings/parameters_weather.html")
            except parameters_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")    
        elif operation=='edit': 
            try:
                data = parameters_weather.objects.get(id=id)
                if request.method == "POST":
                    data.parameter_weather = request.POST.get("parameter_weather")
                    data.save()
                    return HttpResponseRedirect("/settings/lists/")
                else:
                    table_goroda=goroda.objects.all()
                    return render(request, "settings/parameters_weather.html", {"data": data,'table_goroda':table_goroda})
            except parameters_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")                
        elif operation=='delete':
            try:
                data = parameters_weather.objects.get(id=id)
                data.delete()
                return HttpResponseRedirect("/settings/lists/")
            except parameters_weather.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")
