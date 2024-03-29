# Generated by Django 3.2 on 2023-06-04 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trajectory', '0009_airlinesidstarroute_airlinestandardarrival_airlinestandarddeparture'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirlineSidStarWayPointsRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order', models.IntegerField()),
                ('WayPointName', models.CharField(max_length=100)),
                ('LatitudeDegrees', models.FloatField()),
                ('LongitudeDegrees', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AirlineStandardDepartureArrivalRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isSID', models.BooleanField(default=True)),
                ('DepartureArrivalAirport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trajectory.airlineairport')),
                ('DepartureArrivalRunWay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trajectory.airlinerunway')),
                ('FirstLastRouteWayPoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trajectory.airlinewaypoint')),
            ],
        ),
        migrations.RemoveField(
            model_name='airlinestandardarrival',
            name='ArrivalAirport',
        ),
        migrations.RemoveField(
            model_name='airlinestandardarrival',
            name='ArrivalRunWay',
        ),
        migrations.RemoveField(
            model_name='airlinestandardarrival',
            name='LastRouteWayPoint',
        ),
        migrations.RemoveField(
            model_name='airlinestandardarrival',
            name='StandardArrivalRoute',
        ),
        migrations.RemoveField(
            model_name='airlinestandarddeparture',
            name='DepartureAirport',
        ),
        migrations.RemoveField(
            model_name='airlinestandarddeparture',
            name='DepartureRunWay',
        ),
        migrations.RemoveField(
            model_name='airlinestandarddeparture',
            name='FirstRouteWayPoint',
        ),
        migrations.RemoveField(
            model_name='airlinestandarddeparture',
            name='StandardDepartureRoute',
        ),
        migrations.DeleteModel(
            name='AirlineSidStarRoute',
        ),
        migrations.DeleteModel(
            name='AirlineStandardArrival',
        ),
        migrations.DeleteModel(
            name='AirlineStandardDeparture',
        ),
        migrations.AddField(
            model_name='airlinesidstarwaypointsroute',
            name='Route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trajectory.airlinestandarddeparturearrivalroute'),
        ),
    ]
