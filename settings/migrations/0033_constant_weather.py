# Generated by Django 4.2.2 on 2023-09-12 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0032_remove_goroda_and_radio_gorod_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='constant_weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gorod', models.CharField(max_length=80)),
                ('radio', models.CharField(max_length=80)),
            ],
        ),
    ]
