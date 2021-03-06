# Generated by Django 2.2.11 on 2022-02-28 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trajectory', '0003_waypoint_continent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('AirportICAOcode', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('AirportName', models.CharField(max_length=100, unique=True)),
                ('Latitude', models.FloatField()),
                ('Longitude', models.FloatField()),
                ('FieldElevationAboveSeaLevelMeters', models.FloatField()),
                ('Continent', models.CharField(max_length=100)),
            ],
        ),
    ]
