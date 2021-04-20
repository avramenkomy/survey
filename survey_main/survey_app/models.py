from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


def validateQuestionType(value):
    if not value in ['TEXT', 'CHOICE', 'MULTIPLY_CHOICE']:
        raise ValidationError('Invalid question type')


OPTION_TYPES = ['CHOICE', 'MULTIPLE_CHOICE']


# Create your models here.
class Survey(models.Model):
    """ Модель опроса """
    title = models.CharField(verbose_name='Название опроса', unique=True, max_length=255)
    desc = models.CharField(verbose_name='Описание опроса', null=True, max_length=255)
    start_date = models.DateTimeField(verbose_name='Дата старта опроса', default=timezone.now())
    end_date = models.DateTimeField(verbose_name='Дата окончания опроса', default=(timezone.now() + timedelta(days=7)))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    @property
    def is_active(self):
        if (self.start_date < timezone.now()) and (self.end_date > timezone.now()):
            return True
        else:
            return False


class Question(models.Model):
    """ Модель вопроса """
    survey = models.ForeignKey(Survey, verbose_name='Опрос', related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(verbose_name='Текст вопроса', max_length=255)
    # type = models.CharField(verbose_name='Тип вопроса', max_length=30)  # validators=[validateQuestionType]
    type = models.CharField(
        verbose_name='Тип вопроса',
        choices=(
            ("TEXT", "TEXT"),
            ("CHOICE", "CHOICE"),
            ("MULTIPLY_CHOICE", "MULTIPLY_CHOICE"),
        ),
        max_length=30
    )

    def __str__(self):
        return self.text


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', verbose_name='Вопрос', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=300)

    def __str__(self):
        return self.option_text


class Answer(models.Model):
    """Модель ответа на вопрос"""
    user_id = models.CharField(max_length=64)
    survey = models.ForeignKey(Survey, related_name='survey', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    # option = models.ForeignKey(Option, related_name='option', null=True, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.answer_text

class AnonymousUser(models.Model):
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    token = models.CharField(verbose_name='token', max_length=64)

