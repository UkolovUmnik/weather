# Generated by Django 4.2.2 on 2023-09-12 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0025_alter_weather_calendar_day_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weather_calendar',
            old_name='gorod',
            new_name='gorod_id',
        ),
        migrations.RenameField(
            model_name='weather_calendar',
            old_name='radio',
            new_name='radio_id',
        ),
    ]
