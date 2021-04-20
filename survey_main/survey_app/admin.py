from django.contrib import admin
from .models import Survey, Question, Answer, Option, AnonymousUser


# Register your models here.
@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(AnonymousUser)
class AnonymousUserAdmin(admin.ModelAdmin):
    pass
