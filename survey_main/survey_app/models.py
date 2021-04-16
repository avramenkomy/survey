from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


def validateQuestionType(value):
    if not value in ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']:
        raise ValidationError('Invalid question type')


OPTION_TYPES = ['CHOICE', 'MULTIPLE_CHOICE']


# Create your models here.

class Survey(models.Model):
    """ Модель опроса """
    title = models.CharField(verbose_name='Название опроса', unique=True, max_length=255)
    desc = models.CharField(verbose_name='Описание опроса', null=True, max_length=255)
    start_date = models.DateTimeField(verbose_name='Дата старта опроса', default=datetime.now())
    end_date = models.DateTimeField(verbose_name='Дата окончания опроса', default=(datetime.now() + timedelta(days=7)))


class Question(models.Model):
    """ Модель вопроса """
    survey = models.ForeignKey(Survey, verbose_name='Опрос', on_delete=models.CASCADE)
    text = models.CharField(verbose_name='Текст вопроса', max_length=255)
    type = models.CharField(verbose_name='Тип вопроса', max_length=30, validators=[validateQuestionType])
