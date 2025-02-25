# Generated by Django 4.2.2 on 2023-09-11 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0022_goroda_and_radio'),
    ]

    operations = [
        migrations.CreateModel(
            name='weather_calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('gorod', models.CharField(max_length=80)),
                ('radio', models.CharField(max_length=80)),
                ('status_weather', models.BooleanField()),
            ],
        ),
    ]
