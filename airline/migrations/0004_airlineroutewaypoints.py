# Generated by Django 2.2.11 on 2022-03-16 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0003_airlineaircraft'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirlineRouteWayPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order', models.IntegerField()),
                ('WayPoint', models.CharField(max_length=100)),
                ('Route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline.AirlineRoute')),
            ],
        ),
    ]