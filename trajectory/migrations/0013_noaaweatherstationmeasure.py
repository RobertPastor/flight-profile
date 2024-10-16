# Generated by Django 3.2 on 2024-09-21 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trajectory', '0012_noaaweatherstation'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoaaWeatherStationMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LevelFeet', models.FloatField()),
                ('WindSpeedKnots', models.FloatField()),
                ('WindDirectionTrueNorthDegrees', models.FloatField()),
                ('TemperatureDegreesCelsius', models.FloatField()),
                ('NoaaWeatherStationInstance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trajectory.noaaweatherstation')),
            ],
        ),
    ]
