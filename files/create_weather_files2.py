from pydub import AudioSegment
from datetime import datetime
import os
#from datetime import timedelta

max_time_weahterforecast=20
work_directory=os.path.abspath(os.curdir)
weather_segments_dir=work_directory+'\\'+'segments_weather'
directory_for_output_weather_files=work_directory+'\\'+'weather_files'
directory_erros=work_directory+'\\'+'errors'

def create_weather_file_part(weather_segments_dir,dict_parametres):
    cloudy_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'cloudy'+'\\'+dict_parametres.get('cloudy')+'.mp3')
    osadki_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'osadki'+'\\'+dict_parametres.get('osadki')+'.mp3')
    veter_direction_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'veter_direction'+'\\'+dict_parametres.get('veter_direction')+'.mp3')
    veter_speed_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'veter_speed'+'\\'+dict_parametres.get('veter_speed')+'.mp3')
    temperature_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'temperature'+'\\'+dict_parametres.get('temperature')+'.mp3')
    phrase_temparature=AudioSegment.from_mp3(weather_segments_dir+'\\'+'temperature'+'\\'+'temperature.mp3')
    weather_file_part=cloudy_file + osadki_file +veter_direction_file + veter_speed_file + phrase_temparature + temperature_file
    return weather_file_part                                  

def create_weather_file(city, city_on_station, radio, parametrs_weather_current_day,parametrs_weather_tomorrow_day, weekday_today, radio_on_station):
    try:
        oformlenie=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Радио'+'\\'+radio+'\\'+'oformlenie.mp3')
        #по данным нейросети яндекс
        phrase_yandex=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Города'+'\\'+'Яндекс нейросеть.mp3')
        #фраза сегодня в таком-то городе днем                                    
        phrase_today_day_in_city=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Города'+'\\'+city+'\\'+'сегодня.mp3')
        #фраза завтра в таком-то городе днем
        phrase_tomorrow_day_in_city=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Города'+'\\'+city+'\\'+'завтра.mp3')   
        #прогноз погоды
        weather_today_day=create_weather_file_part(weather_segments_dir,parametrs_weather_current_day.get('day'))
        #прогноз погоды
        weather_tomorrow_day=create_weather_file_part(weather_segments_dir,parametrs_weather_tomorrow_day.get('day'))
                                                   
        wheather_today=phrase_yandex+phrase_today_day_in_city+weather_today_day
        wheather_tomorrow=phrase_yandex+phrase_tomorrow_day_in_city+weather_tomorrow_day   

        speaker_timeline_position=0
        with open(weather_segments_dir+'\\'+'Радио'+'\\'+radio+'\\'+'timeline_forecast.txt', encoding='utf-8', mode='r') as file:
            speaker_timeline_position=int(float(file.read())*1000)
##        print('Проблема с файлом позиции погоды')
    
    #делаем экспорт файлов, с наложением на оформление
    #последовательно операции: наложение диктора на подложку, обрезка по времени (отступ по подложке, длительность диктора и 1000 мс это дополнительное время), фейд в конце
        weather_file_today = oformlenie.overlay(wheather_today, position=speaker_timeline_position)[:len(wheather_today)+speaker_timeline_position+1000].fade_out(1000)
        
        weather_file_today.set_frame_rate(44100).export(directory_for_output_weather_files+'\\'+'Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'до'+'.mp3', format='mp3', bitrate="256k")
        print('Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'до'+'.mp3')
                                                   
        weather_file_tomorrow = oformlenie.overlay(wheather_tomorrow, position=speaker_timeline_position)[:len(wheather_today)+speaker_timeline_position+1000].fade_out(1000)
        weather_file_tomorrow.set_frame_rate(44100).export(directory_for_output_weather_files+'\\'+'Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'после'+'.mp3', format='mp3',bitrate="256k")
        print('Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'после'+'.mp3')    

    except Exception as ex:
        current_dateTime_str = datetime.now().strftime('%d-%m-%Y %H:%M')
        if os.path.exists(directory_erros+'\\'+'konstruktor_erros')==False:
            with open(directory_erros+'\\'+'konstruktor_erros.txt',encoding='utf-8',mode="w+") as file:
                pass
        with open(directory_erros+'\\'+'konstruktor_erros.txt',encoding='utf-8',mode="a") as file:
            file.write(city+' '+radio+'\n')
            file.write('Параметры текущего дня: '+str(parametrs_weather_current_day)+'\n')
            file.write('Параметры следующего дня: '+str(parametrs_weather_tomorrow_day)+'\n')
            file.write(current_dateTime_str+' '+str(ex)+'\n')
        return False
    return True


