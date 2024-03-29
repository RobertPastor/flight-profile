# Generated by Django 2.2.11 on 2022-09-03 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=500, unique=True)),
                ('MinLongitudeDegrees', models.FloatField()),
                ('MinLatitudeDegrees', models.FloatField()),
                ('MaxLongitudeDegrees', models.FloatField()),
                ('MaxLatitudeDegrees', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AirlineRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DepartureAirport', models.CharField(max_length=500)),
                ('DepartureAirportICAOCode', models.CharField(max_length=50)),
                ('ArrivalAirport', models.CharField(max_length=500)),
                ('ArrivalAirportICAOCode', models.CharField(max_length=50)),
            ],
            options={
                'unique_together': {('DepartureAirportICAOCode', 'ArrivalAirportICAOCode')},
            },
        ),
        migrations.CreateModel(
            name='AirlineRouteWayPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order', models.IntegerField()),
                ('WayPoint', models.CharField(max_length=100)),
                ('Route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline.AirlineRoute')),
            ],
        ),
        migrations.CreateModel(
            name='AirlineAircraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aircraftICAOcode', models.CharField(max_length=50, unique=True)),
                ('aircraftFullName', models.CharField(max_length=500)),
                ('numberOfAircraftsInService', models.IntegerField(default=0)),
                ('maximumOfPassengers', models.IntegerField(default=0)),
                ('costsFlyingPerHoursDollars', models.FloatField(default=0)),
                ('crewCostsPerFlyingHoursDollars', models.FloatField(default=0)),
                ('landingLengthMeters', models.FloatField(default=0)),
                ('takeOffMTOWLengthMeters', models.FloatField(default=0)),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline.Airline')),
            ],
        ),
    ]
