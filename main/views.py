from datetime import datetime
import os
from calendar import monthrange
import holidays
import shlex #временно для списков urls
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, FileResponse
from main.models import weekdays
from settings.models import goroda,radio,permissions_goroda_and_directions, weather_calendar, goroda_and_radio
from settings.models import names_sections_and_urls #временно для списков urls

from settings.views import check_permission_for_url #проверка разрешений

import main.urls, settings.urls #временно для списков urls

def get_urls_dict(urlpatterns_and_sections):#временно для списков urls
    urls_dict=dict()
    url=[]
    elements_in_url=[]
    for urlpatterns,section in urlpatterns_and_sections:
        for element in urlpatterns: 
            url_element=str(element)
            if url_element.find('URLResolver')==-1:
                elements_in_url=shlex.split(url_element)
                try:
                    name_url=elements_in_url[2]
                except:
                    continue
                name_url=name_url[name_url.find('[')+6:name_url.rfind(']')]
                url=section+elements_in_url[1]
                urls_dict[name_url]=url
    return urls_dict


#проверка разрешения доступа к городу и направлению
def check_permission_gorod_and_direction(user,gorod,direction):
    status=permissions_goroda_and_directions.object.filter(name=user, gorod=gorod, direction=direction).exists()
    return status

def days_in_month():
    date_now=datetime.now()
    days_in_current_month=monthrange(date_now.year,date_now.month)[1]
    list_days_in_month=list(range(1,days_in_current_month+1))
    return days_in_current_month,list_days_in_month

def holidays_in_year():
    for date in holidays.Russia(years=2023).items():
        print(date)

def weekends(): #формирут список дней недели в текущем месяце
    date_Y_and_m=datetime.now().strftime("%Y.%m")
    count_days_in_month,list_days=days_in_month()
##    data=weekdays.objects.all()
##    for element in data:
##        print(element.date)
##        print(element.weekday)
    
    #проверка, есть ли на данный месяц даты и дни недели
    if not weekdays.objects.filter(date=date_Y_and_m+'.01').exists():   
        weekdays_dict={1:"Пн",2:"Вт",3:"Ср",4:"Чт",5:"Пт",6:"Сб",7:"Вс"}
        for i in range(1,count_days_in_month+1):
            if i<10:
                date_str=date_Y_and_m+'.'+'0'+str(i)
            else:
                date_str=date_Y_and_m+'.'+str(i)
            date=datetime.strptime(date_str, '%Y.%m.%d')
            weekday=weekdays_dict.get(datetime.isoweekday(date))
            data=weekdays()
            data.date=date_str
            data.weekday=weekday
            data.save()
    

    weekdays_list=[]
    for i in range(1,count_days_in_month+1):
        if i<10:
            date_str=date_Y_and_m+'.'+'0'+str(i)
        else:
            date_str=date_Y_and_m+'.'+str(i)
        data=weekdays.objects.filter(date=date_str)
        for element in data:
            weekdays_list.append(element.weekday)
    return weekdays_list
                        

@login_required
def index(request):
    #временно для списков urls
    data=names_sections_and_urls.objects.all()
    data.delete()
    
    list_urlpatterns=[main.urls.urlpatterns,settings.urls.urlpatterns]
    list_sections=['','settings/']
    urlpatterns_and_sections=zip(list_urlpatterns,list_sections)
    urls_dict=get_urls_dict(urlpatterns_and_sections)
    for name_url in urls_dict:
        data=names_sections_and_urls()
        data.name_url=name_url
        data.save()
        
    return render(request, "main/index.html")

#@permission_required('blog.add_post', raise_exception=True)
@login_required
def spisok_gorodov(request, requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        list_goroda=[]   
        if request.user.is_superuser:
            table_goroda=goroda.objects.all()
            for element in table_goroda:
                list_goroda.append(element.gorod)
        else:
            username = request.user.username
            table_goroda=permissions_goroda_and_directions.objects.filter(name=username).values('gorod').distinct()
            for element in table_goroda:
                list_goroda.append(element.get('gorod'))
            
        return render(request, "main/spisok_gorodov.html",{"list_goroda":list_goroda})
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")

@login_required
def spisok_radio(request,gorod, requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        list_radio=[]   
        table_radio=goroda_and_radio.objects.filter(gorod=gorod)
        for element in table_radio:
            list_radio.append(element.radio)
        return render(request, "main/spisok_radio.html",{"list_radio":list_radio})
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")

@login_required
def page_weather_calendar(request, gorod, radio, requested_permission):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==True:
        table_weather_calendar=weather_calendar.objects.filter(gorod=gorod,radio=radio)
       
        return render(request, "main/page_weather_calendar.html",{'gorod':gorod,'radio':radio,'table_weather_calendar':table_weather_calendar})
    else:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")


##@login_required
##def update_form_weather_calendar(request, requested_permission, gorod, radio, year, month_number):
##    access_is_allowed=check_permission_for_url(request.user,requested_permission)
##    if access_is_allowed==False:
##        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
##    else:
##        month_dict={'Январь':'01',
##                    'Ферваль':'02',
##                    'Март':'03',
##                    'Апрель':'04',
##                    'Май':'05',
##                    'Июнь':'06',
##                    'Июль':'07',
##                    'Август':'08',
##                    'Сентябрь':'09',
##                    'Октябрь':'10',
##                    'Ноябрь':'11',
##                    'Декарь':'12',
##                    }
####        month_dict={'01':'Январь',
####                    '02':'Ферваль',
####                    '03':'Март',
####                    '04':'Апрель',
####                    '05':'Май',
####                    '06':'Июнь',
####                    '07':'Июль',
####                    '08':'Август',
####                    '09':'Сентябрь',
####                    '10':'Октябрь',
####                    '11':'Ноябрь',
####                    '12':'Декарь',
####                    }
##        year_list=[]
##        year_list.append(str(datetime.now().year))
##        year_list.append(str(datetime.now().year+1))
##
##        days_in_current_month=monthrange(int(year),int(month_number))[1]
##        days_list=list(range(1,days_in_current_month+1))
##        return render(request, "main/weather_interval.html", {'month_dict':month_dict,'year_list':year_list,'days_list':days_list,'month_number_old':month_number,'year_old':year,'gorod':gorod,'radio':radio})
  

@login_required
def change_weather_calendar(request, requested_permission, id, operation, gorod, radio):
    access_is_allowed=check_permission_for_url(request.user,requested_permission)
    if access_is_allowed==False:
        return HttpResponseNotFound("<h2>Доступ запрещен</h2>")
    else:
        month_dict={'Январь':'1',
                    'Ферваль':'2',
                    'Март':'3',
                    'Апрель':'4',
                    'Май':'5',
                    'Июнь':'6',
                    'Июль':'7',
                    'Август':'8',
                    'Сентябрь':'9',
                    'Октябрь':'10',
                    'Ноябрь':'11',
                    'Декарь':'12',
                    }
        year_list=[]
        year_list.append(str(datetime.now().year))
        year_list.append(str(datetime.now().year+1))

        days_in_current_month,days_list=days_in_month()
        #print(days_list)

        if operation=='create':
            try:
                if request.method == "POST":
                    year=request.POST.get("year")
                    #print(year)
                    day_min=int(request.POST.get("day_min"))
                    #print(day_min)
                    day_max=int(request.POST.get("day_max"))
                    #print(day_max)
                    if day_max<day_min:
                        alert='День окончания не может быть меньше, чем день начала'
                        return render(request, "main/weather_interval.html", {'month_dict':month_dict,'year_list':year_list,'days_list':days_list,'gorod':gorod,'radio':radio,'alert':alert})
                    month_number=request.POST.get("month_number")
                    #print(month_number)
                    if int(month_number)<10:
                        month_number = '0'+str(month_number)
                    else:
                        month_number = str(month_number)
                    for day_number in range(day_min,day_max+1):
                        data = weather_calendar()
                        data.year = year
                        data.month = month_number
                        if day_number<10:
                            data.day = '0'+str(day_number)
                        else:
                            data.day = str(day_number)
                        #print(data.day)
                        data.gorod = gorod
                        #print(data.gorod)
                        data.radio = radio
                        #print(data.radio)
                        data.status_weather = request.POST.get("status")
                        #print(data.status)
                        data.save()
                    return HttpResponseRedirect('/pogoda_calendar/'+gorod+'/'+radio+'/')
                else:
                    return render(request, "main/weather_interval.html", {'month_dict':month_dict,'year_list':year_list,'days_list':days_list,'gorod':gorod,'radio':radio})
            except weather_calendar.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")    
        elif operation=='edit': 
            try:
                data = weather_calendar.objects.get(id=id)
                if request.method == "POST":
                    data.date = request.POST.get("date")
                    data.gorod = request.POST.get("gorod")
                    data.radio = request.POST.get("radio")
                    data.status=request.POST.get("status")
                    data.save()
                    return HttpResponseRedirect('/pogoda_calendar/'+gorod+'/'+radio+'/')
                else:
                    return render(request, "main/weather_interval.html", {"data": data,'month_dict':month_dict,'year_list':year_list,'days_list':days_list})
            except weather_calendar.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")                
        elif operation=='delete':
            try:
                data = weather_calendar.objects.get(id=id)
                data.delete()
                return HttpResponseRedirect("/pogoda_calendar/{{gorod}}/{{radio}}/")
            except weather_calendar.DoesNotExist:
                return HttpResponseNotFound("<h2>Данные не найдены</h2>")
 

