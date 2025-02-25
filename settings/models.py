from django.db import models


class goroda(models.Model):
    gorod=models.CharField(max_length=80)
    gorod_on_station=models.CharField(max_length=80)
    gorod_in_yandex_weather=models.CharField(max_length=80)
    gorod_id_yandex_weather=models.CharField(max_length=3,default='000')
    gorod_lat_and_lon=models.CharField(max_length=100,default='000')
    class Meta:
        ordering = ['gorod']

class radio(models.Model):
    radio=models.CharField(max_length=80)
    radio_on_station=models.CharField(max_length=80,default='default')
    class Meta:
        ordering = ['radio']

class goroda_and_radio(models.Model):
    gorod=models.CharField(max_length=80)
    radio=models.CharField(max_length=80)

class weather_calendar(models.Model):
    year=models.CharField(max_length=4)
    month=models.CharField(max_length=2)
    day=models.CharField(max_length=2)
    gorod=models.CharField(max_length=80)
    radio=models.CharField(max_length=80)
    status_weather=models.BooleanField()

class constant_weather(models.Model):
    gorod=models.CharField(max_length=80)
    radio=models.CharField(max_length=80)
    class Meta:
        ordering = ['gorod']


#не заводил для редактирования
class holidays(models.Model):
    date=models.CharField(max_length=10)
    holiday_name=models.CharField(max_length=80)

class permissions_for_urls_groups(models.Model):
    name_group = models.CharField(max_length=80)
    #name_section=models.CharField(max_length=80)
    name_url= models.CharField(max_length=80)

class permissions_for_urls_users(models.Model):
    name_user = models.CharField(max_length=80)
    #name_section=models.CharField(max_length=80)
    name_url= models.CharField(max_length=80)

class names_sections_and_urls(models.Model):
    #name_section = models.CharField(max_length=80)
    name_url= models.CharField(max_length=80)

class permissions_goroda_and_directions(models.Model):
    name= models.CharField(max_length=80)
    gorod=models.CharField(max_length=80)
    direction=models.CharField(max_length=80)

