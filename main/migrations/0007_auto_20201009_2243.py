# Generated by Django 3.0.3 on 2020-10-10 03:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200930_0233'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Fuente',
        ),
        migrations.AlterField(
            model_name='curso',
            name='curso_publicado',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 9, 22, 43, 22, 505890), verbose_name='Fecha de publicacion'),
        ),
    ]