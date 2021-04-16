from django.shortcuts import render
from rest_framework import generics
from .serializers import SurveyDetailSerializer, SurveyListSerializer
from .models import Survey

# Create your views here.

class SurveyCreateView(generics.CreateAPIView):
    serializer_class = SurveyDetailSerializer


class SurveyListView(generics.ListAPIView):
    serializer_class = SurveyListSerializer
    queryset = Survey.objects.all()


class SurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SurveyDetailSerializer
    queryset = Survey.objects.all()
