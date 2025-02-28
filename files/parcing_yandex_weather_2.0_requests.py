import sqlite3
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime, date
from datetime import timedelta
import random
import time
import os
from create_weather_files2 import create_weather_file

logging.basicConfig(level=logging.INFO, filename="log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")

#ruff check parcing_yandex_weather_2.0_requests.py --fix

# logging.debug("A DEBUG Message")
# logging.info("An INFO")
# logging.warning("A WARNING")
# logging.error("An ERROR")
# logging.critical("A message of CRITICAL severity")

WEEKDAYS_DICT={1:'Пн',
              2:'Вт',
              3:'Ср',
              4:'Чт',
              5:'Пт',
              6:'Сб',
              7:'Вс',
        }

WIND_DIRECTION_DICT={'В':'В',
                         'С':'С',
                         'СВ':'СВ',
                         'СЗ':'СЗ',
                         'Ю':'Ю',
                         'ЮВ':'ЮВ',
                         'ЮЗ':'ЮЗ',
                         'З':'З',
        }


def get_radio_dict(cursor : object, name_table : str):
    try:
        radio_dict=dict()
        command="""
            SELECT radio,radio_on_station FROM {name_table}
            """
        cursor.execute(command.format(name_table=name_table))
        result = cursor.fetchall()
        for row in result:
            radio_dict[f"{row[0]}"]={'radio_on_station':f'{row[1]}'}
    except Exception as e:
        logging.warning("Problem with function get_radio_dict"+'\n')
        logging.warning(e+'\n')
        return None
    return radio_dict
   

def check_gorod_for_prognoz_on_date(cursor:object,name_table:str,date_for_prognoz:date,gorod:str):
    try:
        dict_radio=dict()
        year=date_for_prognoz.year
        month=date_for_prognoz.month
        if month<10:
            month='0'+str(month)      
        day=date_for_prognoz.day
        if day<10:
            day='0'+str(day)
        command="""
            SELECT radio,status_weather FROM {name_table} WHERE gorod='{gorod}' AND year='{year}' AND month='{month}' AND day='{day}'
            """
        cursor.execute(command.format(name_table=name_table,gorod=gorod,year=year,month=month,day=day))
        result_command = cursor.fetchall()
        if result_command==[]:
            status_gorod=False
        else:
            status_gorod=True
            for row in result_command:
                dict_radio[f"{row[0]}"]='' 
    except Exception as e:
        logging.warning("Problem with function check_gorod_for_prognoz_on_date"+'\n')
        logging.warning(e+'\n')
        return None
        
    return status_gorod, dict_radio


def get_city_info_from_bd(cursor:object,cities_info:str, cities_list:list=None):
    try:
        if cities_list is None:
            command="""
                SELECT gorod,gorod_on_station,gorod_in_yandex_weather,gorod_lat_and_lon FROM {name_table}
                    """
            cursor.execute(command.format(name_table=cities_info_table))            
        else:   
            command="""
                SELECT gorod_on_station,gorod_in_yandex_weather,gorod_lat_and_lon FROM {name_table} WHERE gorod IN ({cities_list})
                    """
            cursor.execute(command.format(name_table=cities_info, cities_list=cities_list))
        result = cursor.fetchall()
    except Exception as e:
        logging.warning("get_city_info_from_bd")
        logging.warning(e)
        return None
    return result
    

def get_cities_dict(cursor:object,cities_info:str,user_list_cities:list):
    try:
        cities_dict={}
        for row in get_city_info_from_bd(cursor=cursor,cities_info=cities_info, user_list_cities=user_list_cities):
            cities_dict[f'{row[0]}']={'city_on_station':f'{row[1]}','city_in_yandex':f'{row[2]}','lat_and_lon':f'{row[3]}'}   
    except Exception as e:
        logging.warning("get_cities_dict")
        logging.warning(e)
        return None
    return cities_dict

def check_gorod_in_table_constant_weather(cursor:object,name_table:str,gorod:str):
    try:
        dict_radio=dict()
        command="""
            SELECT radio FROM {name_table} WHERE gorod='{gorod}'
            """
        cursor.execute(command.format(name_table=name_table,gorod=gorod))
        result_command = cursor.fetchall()
        if result_command==[]:
            status_gorod=False
        else:
            status_gorod=True
            for row in result_command:
                dict_radio[f"{row[0]}"]=''
    except Exception as e:
        logging.warning("check_gorod_in_table_constant_weather")
        logging.warning(e)
        return None
        
    return status_gorod, dict_radio

def get_dict_goroda_and_radio_for_prognoz(cursor:object,cities_dict:dict,date_for_prognoz):
    try:
        dict_goroda_and_radio_for_prognoz=dict()

        for gorod,_ in cities_dict.items():
            status_gorod_constant_weather,dict_radio_constant_weather=check_gorod_in_table_constant_weather(cursor=cursor,name_table='settings_constant_weather',gorod=gorod) #есть ли город в списке постоянной погоды
            status_gorod_weather,dict_radio_weather=check_gorod_for_prognoz_on_date(cursor=cursor,name_table='settings_weather_calendar',date_for_prognoz=date_for_prognoz,gorod=gorod)

            if status_gorod_constant_weather or status_gorod_weather:
                list_radio=[]
                if dict_radio_constant_weather!={}:
                    for radio in dict_radio_constant_weather.keys():
                        list_radio.append(radio)
                if dict_radio_weather!={}:
                    for radio in dict_radio_weather.keys():
                        if dict_radio_constant_weather.get(radio)==None:
                            list_radio.append(radio)
                dict_goroda_and_radio_for_prognoz[gorod]=list_radio

    except Exception as e:
        logging.warning("get_dict_goroda_and_radio_for_prognoz"+'\n')
        logging.warning(e+'\n')
        return None
   
    return dict_goroda_and_radio_for_prognoz

    #на сайте если радио уже в постоянной погоде, то убрать возможность ставить сроки

#bkn-m-ra-n
#bkn-m-sn-d m-небольшой
#ovc-ts-ra дождь с грозой
#ovc-ra дождь
#ts гроза
#ovc-ra-sn дождь со снегом
#ovc-p-sn сильный снег
#ovc-sn-d    
def get_cloudy_and_osadki(cloudy_and_osadki_list,cloudy_or_osadki_parametr):
    #словари с table, это параметр в таблице, в котором или осадки или облачность. Сначала проверяем по нему, если нет нужных значений, тогда по картинке
    osadki=None
    cloudy=None
    #print('Общий параметр '+cloudy_or_osadki_parametr)
    #print('Картинка '+str(cloudy_and_osadki_list))

    dict_cloudy_table={'Пасмурно':'Пасмурно',
                'Облачно с прояснениями':'Переменная_облачность',       
                'Малооблачно':'Малооблачно',
                'Ясно':'Ясно'
                 }
    
    dict_osadki_table={'Дождь':'Дождь',
                'Небольшой дождь':'Небольшой_дождь',
                'Небольшой снег':'Небольшой_снег',
                'Ливень':'Ливень',
                'Ливни':'Ливень',
                'Дождь с грозой':'Дождь_с_грозой'                    
        }
    

    dict_cloudy_image={'bkn':'Переменная_облачность',
                'ovc':'Пасмурно',
                'skc':'Ясно'
                 }


    dict_osadki_image={'ra':'Дождь',
                'p-ra':'Ливень',
                'm-ra':'Небольшой_дождь',
                'sn':'Снег',
                'm-sn':'Небольшой_снег',
                'p-sn':'Снегопад',
                'ra-sn':'Дождь_со_снегом',
                'ts':'Гроза',                      
        }

    #проверяем облачность и осадки по общему параметру
    cloudy=dict_cloudy_table.get(cloudy_or_osadki_parametr)
    #print('Cloudy по общему параметру '+str(cloudy))
    if cloudy is None:
        osadki=dict_osadki_table.get(cloudy_or_osadki_parametr)
        #print('Осадки по общему параметру '+str(osadki))

    #проверка облачности по картинке
    if cloudy is None:                 
        cloudy=dict_cloudy_image.get(cloudy_and_osadki_list[0])
        #print('Cloudy по картинке '+str(cloudy))
        
    #проверка осадков по картинке
    if osadki==None:
        #print('Количество элементов в списке '+str(len(cloudy_and_osadki_list)))
        if len(cloudy_and_osadki_list)==1:
            osadki='Без-осадков'
            #print('Осадки по картинке '+osadki)
        else:
            osadki=dict_osadki_image.get(cloudy_and_osadki_list[1])
            #print('Осадки по картинке '+str(osadki)) 
    
    return cloudy, osadki

def get_parametres_from_weather_table(table_element,number_row_in_table):
    #1 столбец - обозначения в яндекс погоде, 2 - названия файлов для конструктора

    row=table_element.find_all('tr',recursive=False)[number_row_in_table-1]
    try:
        wind_block=row.find_all('td',recursive=False)[5]
        wind_speed=wind_block.find('span',class_='wind-speed').text
        wind_speed=round(float(wind_speed.replace(',','.')))
        if wind_speed==0:
            wind_speed=1
        wind_speed=str(wind_speed)
        print('Скорость ветра= '+wind_speed)
        wind_direction=wind_block.find('div',class_='weather-table__wind-direction').abbr.text
        wind_direction=WIND_DIRECTION_DICT.get(wind_direction)
        print('Направление ветра= '+str(wind_direction))
    except AttributeError:
        wind_speed=wind_block.find('span',class_='weather-table__wind').text
        #костыль, чтобы программа не сбивалась
        if wind_speed=='Штиль':
            wind_speed='1'
            wind_direction='З'
    print('Прошел ветер')
    try:
        #когда в таблице указана вилка температур
        t_max=row.find_all('td',recursive=False)[0].find('div',class_='weather-table__temp').span.text
        temperature=t_max
        print(f'Стандартный случай t: {t_max}')
        if ord(temperature[0])==8722: #8722-это код минуса в html кодировке, заменяем его на обычный в кодировке utf-8
            temperature=temperature.replace(temperature[0],'-')
    except:
        #случай, когда одна температура указана
        t_max=row.find_all('td',recursive=False)[0].find('div',class_='weather-table__temp').span.text
        temperature=t_max
        print(f'Нестандартный случай t: {t_max}')
        if ord(temperature[0])==8722: #8722-это код минуса в html кодировке, заменяем его на обычный в кодировке utf-8
            temperature=temperature.replace(temperature[0],'-')

    temperature=str(int(temperature))
    print('Прошел температуру')

    na_nebe_class_image=row.find_all('td',recursive=False)[1].img.get('class')
    na_nebe_class_image=na_nebe_class_image[1].replace('icon_thumb_','').replace('-d','').replace('-n','').split('-',1)
    print('Класс картинки= '+str(na_nebe_class_image))

    cloudy_or_osadki_parametr=row.find_all('td',recursive=False)[2].text
    print('Облачность или осадки= '+cloudy_or_osadki_parametr)
    cloudy, osadki =  get_cloudy_and_osadki(na_nebe_class_image,cloudy_or_osadki_parametr)
    print('Прошел облачность и осадки')
    #подумать, как сделать, если в будущем будут появляться новые значения, чтобы их заносить, узнавать об этом (в файлы записывать и т.д.)

    dict_paremetres=dict()
    dict_paremetres['cloudy']=cloudy
    dict_paremetres['osadki']=osadki
    dict_paremetres['veter_speed']=wind_speed
    dict_paremetres['veter_direction']=wind_direction
    dict_paremetres['temperature']=temperature
     
    return dict_paremetres

def get_response(lat_and_lon:str)->object:
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'})
    url=f'https://yandex.ru/pogoda/segment/details?{lat_and_lon}&cameras=0' 
    response=requests.get(url) 
    return response

def get_parametres_dict_from_response(response:object,numbers_days_for_prognoz_dict:dict):

    soup = BeautifulSoup(response.text, "html.parser")
    print('Загрузил страницу')

    cards=soup.findAll('article',class_='card')
    print(f'Количество найденных таблиц: {len(cards)}')
    parametres_dict=dict()
    for card in cards:
        if card.get('class')!=['card']:
            continue
        day=card.find_all('div',recursive=False)[0].get('id')
        if day=='': continue
        day_number=day.split('_')[1]
        #print(day_number)
        if numbers_days_for_prognoz_dict.get(day_number)!=None: continue

        table_with_parametres=card.find_all('div',recursive=False)[1].tbody
        day_parametres=get_parametres_from_weather_table(table_with_parametres,2)
        parametres_dict[day_number]={'day':day_parametres}
        numbers_days_for_prognoz_dict[day_number]=True
        status_end=True
        for _,status in numbers_days_for_prognoz_dict.items():
            if status==False:
                status_end=False
                break
        print('Итоговый статус'+str(status_end))
        if status_end==True:
            break                              
    return parametres_dict

def get_data_for_gorod(lat_and_lon:str,numbers_days_for_prognoz_dict:dict):

    for day_number_str,status in numbers_days_for_prognoz_dict.items():
        numbers_days_for_prognoz_dict[day_number_str]=False

    response=get_response(lat_and_lon)
    #print(response.status_code)
    
    parametres_dict=get_parametres_dict_from_response(response,numbers_days_for_prognoz_dict)

    return parametres_dict

def connect_bd(path:str):
    print(path)
    #work_dir=os.path.abspath(os.curdir)
    #db_file=work_dir[:work_dir.rfind('\\')+1]+'db.sqlite3'
    connection = sqlite3.connect(path)
    return connection

def get_settings_for_create_files(cursor:object, count_of_days_prognoz:int, cities_dict:dict):
    try:
        settings_for_create_files=[]
        numbers_days_for_prognoz={}
        current_date_and_time=datetime.now()-timedelta(days=1) 
        print(current_date_and_time.strftime("%d.%m.%Y"))

        for number_day_prognoz in range(1,count_of_days_prognoz+1):
            current_date_and_time+=timedelta(days=1)
            tomorrow_date_and_time=current_date_and_time+timedelta(days=1)
            settings_for_create_files.append({'current_day':str(current_date_and_time.day),
                                              'tomorrow_day':str(tomorrow_date_and_time.day),
                                              'weekday':WEEKDAYS_DICT.get(current_date_and_time.isoweekday()),
                                              'dict_goroda_and_radio_for_prognoz':get_dict_goroda_and_radio_for_prognoz(cursor=cursor,
                                                                                    cities_dict=cities_dict,date_for_prognoz=current_date_and_time)})
            numbers_days_for_prognoz[str(current_date_and_time.day)]=False
        numbers_days_for_prognoz[str(tomorrow_date_and_time.day)]=False
    except Exception as e:
        logging.warning("get_settings_for_create_files")
        logging.warning(e)
        return None, None
    return settings_for_create_files, numbers_days_for_prognoz

def get_all_data(cities_dict:dict,numbers_days_for_prognoz_dict:dict)->dict:
    parametres_dict_all=dict()
    for city,_ in cities_dict.items():
        print(city)
        lat_and_lon=cities_dict.get(city).get('lat_and_lon')
        parametres_dict=get_data_for_gorod(lat_and_lon=lat_and_lon,numbers_days_for_prognoz_dict=numbers_days_for_prognoz_dict)
        pauze_time=random.randint(5, 10)
        time.sleep(pauze_time)
        parametres_dict_all[city]=parametres_dict
        print(parametres_dict)
    return parametres_dict_all


def run_konstruktor(settings_for_create_files:list,cities_dict:dict,radio_dict:dict,parametres_dict_all:dict):
    for prognoz_settings in settings_for_create_files:
        print(prognoz_settings.get('weekday'))              
        for gorod, list_radio in prognoz_settings.get('dict_goroda_and_radio_for_prognoz').items():
            print(gorod)

            parametrs_weather_on_days_for_gorod=parametres_dict_all.get(gorod)
            if parametrs_weather_on_days_for_gorod==None:
                print('Не удалось получить город '+str(gorod))
                continue
            parametrs_weather_current_day=parametrs_weather_on_days_for_gorod.get(prognoz_settings.get('current_day'))
            parametrs_weather_tomorrow_day=parametrs_weather_on_days_for_gorod.get(prognoz_settings.get('tomorrow_day'))
            gorod_on_station=cities_dict.get(gorod).get('city_on_station')
            for radio in list_radio:
                radio_on_station=radio_dict.get(radio).get('radio_on_station')
                create_weather_file(gorod, gorod_on_station, radio, parametrs_weather_current_day,parametrs_weather_tomorrow_day, prognoz_settings.get('weekday'), radio_on_station)

def main(count_of_days_prognoz:int, user_list_cities:list=None):
    connection = connect_bd("../db.sqlite3")
    cursor = connection.cursor()
    
    cities_dict=get_cities_dict(cursor,'settings_goroda',user_list_cities)
    print(cities_dict)
    radio_dict=get_radio_dict(cursor,'settings_radio')
    settings_for_create_files,numbers_days_for_prognoz=get_settings_for_create_files(cursor=cursor,count_of_days_prognoz=count_of_days_prognoz, cities_dict=cities_dict)
    parametres_dict_all=get_all_data(cities_dict=cities_dict,numbers_days_for_prognoz_dict=numbers_days_for_prognoz)

    print('начинаю сборку')
    run_konstruktor(settings_for_create_files,cities_dict,radio_dict,parametres_dict_all)
    if connection:
        connection.close()
#добавить на сайт колонку к городам назваие на станции, и в создание файлов учесть        
try:
    main(count_of_days_prognoz=7, user_list_cities=['Пятигорск','Есентуки'])
    #проверка на count_of_days при ручном вводе
except Exception as e:
    print(e)
input()
