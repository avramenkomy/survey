# Generated by Django 2.2.10 on 2021-04-19 17:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0002_auto_20210419_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='option_text',
            new_name='answer_text',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='option',
        ),
        migrations.AlterField(
            model_name='survey',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 26, 19, 59, 38, 167218), verbose_name='Дата окончания опроса'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 19, 19, 59, 38, 167168), verbose_name='Дата старта опроса'),
        ),
    ]
