# Generated by Django 2.2.11 on 2023-03-04 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0005_airlinecosts'),
    ]

    operations = [
        migrations.AddField(
            model_name='airlinecosts',
            name='finalLengthMeters',
            field=models.FloatField(default=0),
        ),
    ]
