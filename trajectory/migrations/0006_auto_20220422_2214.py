# Generated by Django 2.2.11 on 2022-04-22 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trajectory', '0005_runway'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Airport',
            new_name='AirlineAirport',
        ),
        migrations.RenameModel(
            old_name='RunWay',
            new_name='AirlineRunWay',
        ),
        migrations.RenameModel(
            old_name='WayPoint',
            new_name='AirlineWayPoint',
        ),
        migrations.RenameModel(
            old_name='Aircraft',
            new_name='BadaSynonymAircraft',
        ),
    ]