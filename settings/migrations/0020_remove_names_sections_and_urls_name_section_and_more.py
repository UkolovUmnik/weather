# Generated by Django 4.2.2 on 2023-08-25 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0019_alter_names_sections_and_urls_name_section_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='names_sections_and_urls',
            name='name_section',
        ),
        migrations.RemoveField(
            model_name='permissions_for_urls_groups',
            name='name_section',
        ),
        migrations.RemoveField(
            model_name='permissions_for_urls_users',
            name='name_section',
        ),
    ]
