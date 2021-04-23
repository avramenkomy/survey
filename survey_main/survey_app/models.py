from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


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
    type = models.CharField(
        verbose_name='Тип вопроса',
        choices=(
            ("TEXT", "TEXT"),
            ("CHOICE", "CHOICE"),
            ("MULTIPLY_CHOICE", "MULTIPLY_CHOICE"),
        ),
        max_length=30
    )
    variant_answer_1 = models.CharField(verbose_name='Вариант ответа 1', max_length=255, null=True, default=None)
    variant_answer_2 = models.CharField(verbose_name='Вариант ответа 2', max_length=255, null=True, default=None)
    variant_answer_3 = models.CharField(verbose_name='Вариант ответа 3', max_length=255, null=True, default=None)
    variant_answer_4 = models.CharField(verbose_name='Вариант ответа 4', max_length=255, null=True, default=None)

    def __str__(self):
        return self.text


class Answer(models.Model):
    """Модель ответа на вопрос"""
    user_id = models.CharField(max_length=64)
    survey = models.ForeignKey(Survey, related_name='survey', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.answer_text


class AnonymousUser(models.Model):
    """Модель для анонимного пользователя"""
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    token = models.CharField(verbose_name='token', max_length=64)
