# Generated by Django 2.2.11 on 2022-03-12 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0002_auto_20220309_2050'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirlineAircraft',
            fields=[
                ('aircraftICAOcode', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('aircraftFullName', models.CharField(max_length=500)),
                ('numberOfAircraftsInService', models.IntegerField(default=0)),
                ('maximumOfPassengers', models.IntegerField(default=0)),
                ('costsFlyingPerHoursDollars', models.FloatField(default=0)),
                ('landingLengthMeters', models.FloatField(default=0)),
                ('takeOffMTOWLengthMeters', models.FloatField(default=0)),
            ],
        ),
    ]
