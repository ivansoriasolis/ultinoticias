# Generated by Django 3.0.3 on 2020-10-10 06:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20201009_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='curso_publicado',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 10, 1, 37, 0, 654687), verbose_name='Fecha de publicacion'),
        ),
    ]