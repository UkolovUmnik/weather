from pydub import AudioSegment
from datetime import datetime
import os
import logging
#from datetime import timedelta

max_time_weahterforecast=20
# work_directory=os.path.abspath(os.curdir)
# weather_segments_dir=work_directory+'\\'+'segments_weather'
weather_segments_dir='../segments_weather'
# output_directory=work_directory+'\\'+'weather_files'
output_directory='../weather_files'
# directory_erros=work_directory+'\\'+'errors'
directory_erros='../errors'

def create_weather_file_part(weather_segments_dir:str,dict_parametres:dict,need_parameteres_list:list):
    weather_file_part=AudioSegment.empty()
    try:
        if 'Облачность' in need_parameteres_list:
            cloudy_file = AudioSegment.from_mp3(weather_segments_dir+'/cloudy/'+dict_parametres.get('cloudy')+'.mp3')
            weather_file_part+=cloudy_file
        if 'Осадки' in need_parameteres_list:
            osadki_file = AudioSegment.from_mp3(weather_segments_dir+'/osadki/'+dict_parametres.get('osadki')+'.mp3')
            weather_file_part+=osadki_file
        if 'Направление ветра' in need_parameteres_list:
            veter_direction_file = AudioSegment.from_mp3(weather_segments_dir+'/veter_direction/'+dict_parametres.get('veter_direction')+'.mp3')
            weather_file_part+=veter_direction_file
        if 'Скорость ветра' in need_parameteres_list:
            veter_speed_file = AudioSegment.from_mp3(weather_segments_dir+'/veter_speed/'+dict_parametres.get('veter_speed')+'.mp3')
            weather_file_part+=veter_speed_file
        if 'Температура' in need_parameteres_list:
            temperature_file = AudioSegment.from_mp3(weather_segments_dir+'/temperature/'+dict_parametres.get('temperature')+'.mp3')
            phrase_temparature = AudioSegment.from_mp3(weather_segments_dir+'/temperature/temperature.mp3')
            weather_file_part+=phrase_temparature+temperature_file
    except Exception as e:
        logging.warning("function create_weather_file_part()")
        logging.warning(e)
        return None
    return weather_file_part 

def create_weather_file(city, city_on_station, radio, parametrs_weather_current_day,parametrs_weather_tomorrow_day, weekday_today, radio_on_station, goroda_additionally):
    try:
        oformlenie=AudioSegment.from_mp3(weather_segments_dir+'/Радио/'+radio+'/oformlenie.mp3')
        #по данным нейросети яндекс
        phrase_yandex=AudioSegment.from_mp3(weather_segments_dir+'/Города/Яндекс нейросеть.mp3')
        #фраза сегодня в таком-то городе днем                                    
        phrase_today_day_in_city=AudioSegment.from_mp3(weather_segments_dir+'/Города/'+city+'/сегодня.mp3')
        #фраза завтра в таком-то городе днем
        phrase_tomorrow_day_in_city=AudioSegment.from_mp3(weather_segments_dir+'/Города/'+city+'/завтра.mp3')   
        #прогноз погоды
        weather_today_day_main=create_weather_file_part(weather_segments_dir,parametrs_weather_current_day.get('day'))
        #прогноз погоды
        weather_tomorrow_day_main=create_weather_file_part(weather_segments_dir,parametrs_weather_tomorrow_day.get('day'))
        
        wheather_today=phrase_yandex+phrase_today_day_in_city+weather_today_day_main
        wheather_tomorrow=phrase_yandex+phrase_tomorrow_day_in_city+weather_tomorrow_day_main

        if goroda_additionally!=None:
            for gorod_additionally in goroda_additionally:
                wheather_today+=AudioSegment.from_mp3(weather_segments_dir+'/Города/Доп города/'+gorod_additionally+'/gorod.mp3')
                wheather_today+=create_weather_file_part(weather_segments_dir,parametres_dict_all.get(gorod_additionally).get(current_day).get('day'),need_parameteres_all_dict.get(gorod_additionally))
                wheather_tomorrow+=AudioSegment.from_mp3(weather_segments_dir+'/Города/Доп города/'+gorod_additionally+'/gorod.mp3')
                wheather_tomorrow+=create_weather_file_part(weather_segments_dir,parametres_dict_all.get(gorod_additionally).get(tomorrow_day).get('day'),need_parameteres_all_dict.get(gorod_additionally))
                                                   

        speaker_timeline_position=0
        with open(weather_segments_dir+'/Радио/'+radio+'/timeline_forecast.txt', encoding='utf-8', mode='r') as file:
            speaker_timeline_position=int(float(file.read())*1000)
    
    #делаем экспорт файлов, с наложением на оформление
    #последовательно операции: наложение диктора на подложку, обрезка по времени (отступ по подложке, длительность диктора и 1000 мс это дополнительное время), фейд в конце
        weather_file_today = oformlenie.overlay(wheather_today, position=speaker_timeline_position)[:len(wheather_today)+speaker_timeline_position+1000].fade_out(1000)
        
        weather_file_today.set_frame_rate(44100).export(output_directory+'/Погода_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_до'+'.mp3', format='mp3', bitrate="256k")
        print('Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'до'+'.mp3')
                                                   
        weather_file_tomorrow = oformlenie.overlay(wheather_tomorrow, position=speaker_timeline_position)[:len(wheather_today)+speaker_timeline_position+1000].fade_out(1000)
        weather_file_tomorrow.set_frame_rate(44100).export(output_directory+'/Погода_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'после'+'.mp3', format='mp3',bitrate="256k")
        print('Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'после'+'.mp3')    

    except Exception as e:
        logging.warning("function create_weather_file()")
        logging.warning(city+' '+radio)
        logging.warning('Параметры текущего дня: '+str(parametrs_weather_current_day))
        logging.warning('Параметры следующего дня: '+str(parametrs_weather_tomorrow_day))
        logging.warning(e)
        return False
    return True