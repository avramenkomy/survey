from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "survey_app"
urlpatterns = [
    path('users/', UserAllView.as_view()),

    path('survey/', SurveyAllView.as_view()), # get all survey
    path('survey/active/', SurveyActiveView.as_view()), # get all active survey
    path('survey/create/', SurveyCreateView.as_view()), # create survey
    path('survey/update/<int:pk>', SurveyUpdateView.as_view()), # update survey
    path('survey/delete/<int:pk>', SurveyDeleteView.as_view()), # delete survey
    path('survey/detail/<int:pk>', SurveyDetailView.as_view()), # detail survey

    path('question/', QuestionView.as_view()), # get all question
    path('question/create/', QuestionCreateView.as_view()), # create question
    path('question/update/<int:pk>', QuestionUpdateView.as_view()), # update question
    path('question/delete/<int:pk>', QuestionDeleteView.as_view()), # delete question

    path('answer/create/<int:pk>', AnswerCreateView.as_view()), # create answer
    path('answer/<int:pk>', AnswerView.as_view()),
    path('answer/<int:pk_user>/<int:pk_survey>', AnswerWithSurvey.as_view()),
    path('answer/my_answer/', AnswerByUserView.as_view()), # get answers for than user

]
