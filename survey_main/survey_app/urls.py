from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = "survey_app"
urlpatterns = [
    path('survey/create/', SurveyCreateView.as_view()), # создание опроса
    path('survey/', SurveyListView.as_view()), # Список всех опросов
    path('survey/detail/<int:pk>', SurveyDetailView.as_view()), # просмотр опроса
]
