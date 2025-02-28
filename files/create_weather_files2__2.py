from pydub import AudioSegment
from datetime import datetime
import os
#from datetime import timedelta

max_time_weahterforecast=20
work_directory=os.path.abspath(os.curdir)
weather_segments_dir=work_directory+'\\'+'segments_weather'
directory_for_output_weather_files=work_directory+'\\'+'weather_files'
directory_erros=work_directory+'\\'+'errors'

def create_weather_file_part(weather_segments_dir,dict_parametres,need_parameteres_dict):
    weather_file_part=AudioSegment.empty()
    try:
        if need_parameteres_dict.get('Облачность')!=None:
            weather_file_part+=AudioSegment.from_mp3(weather_segments_dir+'\\'+'cloudy'+'\\'+dict_parametres.get('cloudy')+'.mp3')
        if need_parameteres_dict.get('Осадки')!=None:
            weather_file_part+=AudioSegment.from_mp3(weather_segments_dir+'\\'+'osadki'+'\\'+dict_parametres.get('osadki')+'.mp3')
        if need_parameteres_dict.get('Направление ветра')!=None:
            weather_file_part+=AudioSegment.from_mp3(weather_segments_dir+'\\'+'veter_direction'+'\\'+dict_parametres.get('veter_direction')+'.mp3') 
        if need_parameteres_dict.get('Скорость ветра')!=None:
            weather_file_part+=AudioSegment.from_mp3(weather_segments_dir+'\\'+'veter_speed'+'\\'+dict_parametres.get('veter_speed')+'.mp3')
        if need_parameteres_dict.get('Температура')!=None:
            weather_file_part+=AudioSegment.from_mp3(weather_segments_dir+'\\'+'temperature'+'\\'+'temperature.mp3')
            weather_file_part+=AudioSegment.from_mp3(weather_segments_dir+'\\'+'temperature'+'\\'+dict_parametres.get('temperature')+'.mp3')
            
            
##        cloudy_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'cloudy'+'\\'+dict_parametres.get('cloudy')+'.mp3')
##        osadki_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'osadki'+'\\'+dict_parametres.get('osadki')+'.mp3')
##        veter_direction_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'veter_direction'+'\\'+dict_parametres.get('veter_direction')+'.mp3')
##        veter_speed_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'veter_speed'+'\\'+dict_parametres.get('veter_speed')+'.mp3')
##        temperature_file = AudioSegment.from_mp3(weather_segments_dir+'\\'+'temperature'+'\\'+dict_parametres.get('temperature')+'.mp3')
##        phrase_temparature=AudioSegment.from_mp3(weather_segments_dir+'\\'+'temperature'+'\\'+'temperature.mp3')
##        weather_file_part=cloudy_file + osadki_file +veter_direction_file + veter_speed_file + phrase_temparature + temperature_file
        return weather_file_part
    except Exception as ex:
        if os.path.exists(directory_erros+'\\'+'konstruktor_erros')==False:
            with open(directory_erros+'\\'+'konstruktor_erros',encoding='utf-8',mode="w+") as file:
                file.write(str(ex)+'\n')
        else:
            with open(directory_erros+'\\'+'konstruktor_erros',encoding='utf-8',mode="a") as file:
                file.write(str(ex)+'\n')
        return None


#cross fade
#with_style = beginning.append(end, crossfade=1500)
# 2 sec fade in, 3 sec fade out
#awesome = do_it_over.fade_in(2000).fade_out(3000)                                  

def create_weather_files(city, city_on_station, radio, parametres_dict_all, weekday_today, radio_on_station, need_parameteres_all_dict,goroda_additionally,current_day,tomorrow_day):
    print(parametres_dict_all)
    print(goroda_additionally)
    print(need_parameteres_all_dict)
    
    #файл с офорлением (музыка станции на фоне)
    try:
        oformlenie=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Радио'+'\\'+radio+'\\'+'oformlenie.mp3')
    except Exception as ex:
        with open(directory_erros+'\\'+'konstruktor_erros',encoding='utf-8',mode="a") as file:
            file.write(str(ex))
            print('\n')
        return None

    try:
        #для основного города
        #по данным нейросети яндекс
        phrase_yandex=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Города'+'\\'+'Яндекс нейросеть.mp3')

        #фраза сегодня в таком-то городе                                   
        phrase_today_day_in_city=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Города'+'\\'+city+'\\'+'сегодня.mp3')

        #использовать need_parameteres_all_dict для городов!!!!!!

        #фраза завтра в таком-то городе днем
        phrase_tomorrow_day_in_city=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Города'+'\\'+city+'\\'+'завтра.mp3')   
            
    except Exception as ex:
        with open(directory_erros+'\\'+'konstruktor_erros',encoding='utf-8',mode="a") as file:
            file.write(str(ex)+'\n')
        return None
    
    #прогноз погоды
    weather_today_day_for_main_gorod=create_weather_file_part(weather_segments_dir,parametres_dict_all.get(city).get(current_day).get('day'),need_parameteres_all_dict.get(city))
##    if weather_today_day==None:
##        return None

    weather_tomorrow_day_for_main_gorod=create_weather_file_part(weather_segments_dir,parametres_dict_all.get(city).get(tomorrow_day).get('day'),need_parameteres_all_dict.get(city))
##    if weather_tomorrow_day==None:
##        return None

    
    wheather_today=phrase_yandex+phrase_today_day_in_city+weather_today_day_for_main_gorod
    wheather_tomorrow=phrase_yandex+phrase_tomorrow_day_in_city+weather_tomorrow_day_for_main_gorod
    if goroda_additionally!=None:
        for gorod_additionally in goroda_additionally:
            wheather_today+=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Города'+'\\'+'Доп города'+'\\'+gorod_additionally+'\\'+'gorod.mp3')
            wheather_today+=create_weather_file_part(weather_segments_dir,parametres_dict_all.get(gorod_additionally).get(current_day).get('day'),need_parameteres_all_dict.get(gorod_additionally))
            wheather_tomorrow+=AudioSegment.from_mp3(weather_segments_dir+'\\'+'Города'+'\\'+'Доп города'+'\\'+gorod_additionally+'\\'+'gorod.mp3')
            wheather_tomorrow+=create_weather_file_part(weather_segments_dir,parametres_dict_all.get(gorod_additionally).get(tomorrow_day).get('day'),need_parameteres_all_dict.get(gorod_additionally))    

    file_timeline_forecast=weather_segments_dir+'\\'+'Радио'+'\\'+radio+'\\'+'timeline_forecast.txt'
    if not os.path.isfile(file_timeline_forecast):
        position=0
    else:
        try:
            with open(weather_segments_dir+'\\'+'Радио'+'\\'+radio+'\\'+'timeline_forecast.txt', encoding='utf-8', mode='r') as file:
                for line in file:
                    speaker_timeline_position=int(float(line)*1000)
        except Exception as ex:
            print('Проблема с файлом позиции погоды')
            print(str(ex))
            with open(directory_erros+'\\'+'konstruktor_erros',encoding='utf-8',mode="a") as file:
                file.write(str(ex)+'\n')
    
    #делаем экспорт файлов, с наложением на оформление
##    weather_file_today = oformlenie.overlay(wheather_today, position=speaker_timeline_position)[:max_time_weahterforecast*1000].fade_out(2000)
##    
##    weather_file_today.export(directory_for_output_weather_files+'\\'+'Погода'+'_'+city+'_'+radio+'_'+weekday_today+'_'+'до'+'.mp3', format='mp3')
##    print(directory_for_output_weather_files+'\\'+'Погода'+'_'+city+'_'+radio+'_'+weekday_today+'_'+'до'+'.mp3')
##    
##    weather_file_tomorrow = oformlenie.overlay(wheather_tomorrow, position=speaker_timeline_position)[:max_time_weahterforecast*1000].fade_out(2000)
##    weather_file_tomorrow.export(directory_for_output_weather_files+'\\'+'Погода'+'_'+city+'_'+radio+'_'+weekday_today+'_'+'после'+'.mp3', format='mp3')
##    print(directory_for_output_weather_files+'\\'+'Погода'+'_'+city+'_'+radio+'_'+weekday_today+'_'+'после'+'.mp3')


    #делаем экспорт файлов, с наложением на оформление
    #последовательно операции: наложение диктора на подложку, обрезка по времени (отступ по подложке, длительность диктора и 1000 мс это дополнительное время), фейд в конце
    weather_file_today = oformlenie.overlay(wheather_today, position=speaker_timeline_position)[:len(wheather_today)+speaker_timeline_position+1000].fade_out(1000)
    
    weather_file_today.set_frame_rate(44100).export(directory_for_output_weather_files+'\\'+'Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'до'+'.mp3', format='mp3', bitrate="256k")
    print(directory_for_output_weather_files+'\\'+'Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'до'+'.mp3')
    
    weather_file_tomorrow = oformlenie.overlay(wheather_tomorrow, position=speaker_timeline_position)[:len(wheather_today)+speaker_timeline_position+1000].fade_out(1000)
    weather_file_tomorrow.set_frame_rate(44100).export(directory_for_output_weather_files+'\\'+'Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'после'+'.mp3', format='mp3',bitrate="256k")
    #weather_file_tomorrow.set_frame_rate(44100).export(directory_for_output_weather_files+'\\'+'Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'после'+'.mp3', format='mp3',bitrate="256k")
    print(directory_for_output_weather_files+'\\'+'Погода'+'_'+city_on_station+'_'+radio_on_station+'_'+weekday_today+'_'+'после'+'.mp3')    

    return True


