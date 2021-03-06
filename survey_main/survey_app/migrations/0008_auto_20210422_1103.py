# Generated by Django 2.2.10 on 2021-04-22 08:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('survey_app', '0007_auto_20210420_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='variant_answer_1',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='Вариант ответа 1'),
        ),
        migrations.AddField(
            model_name='question',
            name='variant_answer_2',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='Вариант ответа 2'),
        ),
        migrations.AddField(
            model_name='question',
            name='variant_answer_3',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='Вариант ответа 3'),
        ),
        migrations.AddField(
            model_name='question',
            name='variant_answer_4',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='Вариант ответа 4'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 29, 8, 3, 26, 82888, tzinfo=utc), verbose_name='Дата окончания опроса'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 22, 8, 3, 26, 82888, tzinfo=utc), verbose_name='Дата старта опроса'),
        ),
    ]
