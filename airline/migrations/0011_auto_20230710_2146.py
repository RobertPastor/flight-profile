# Generated by Django 3.2 on 2023-07-10 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0010_auto_20230709_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='firstCnxDateTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastCnxDateTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]