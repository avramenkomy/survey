from rest_framework import serializers
from .models import Survey


# Для создания записи в БД создаем сериализатор опросов:
class SurveyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

# start_date = serializers.HiddenField(default=serializers.CurrentUserDefault())
