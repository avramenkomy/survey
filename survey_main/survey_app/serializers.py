from rest_framework import serializers
from .models import Survey, Question, Answer, User, Option
from rest_framework.serializers import ValidationError


def validateQuestionType(value):
    if not value in ['TEXT', 'CHOICE', 'MULTIPLY_CHOICE']:
        raise ValidationError('Invalid question type')


# Сериализатор вопроса
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionOneFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("text", "type",)


# сериализатор для просмотра активных опросов с вопросами
class SurveyActiveSerializer(serializers.ModelSerializer):
    questions = QuestionOneFieldSerializer(many=True)

    class Meta:
        model = Survey
        fields = '__all__'


# сериализатор для просмотра опроса
class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyUpdateSerializer(serializers.ModelSerializer):
    start_date = serializers.ReadOnlyField(default=SurveySerializer())

    class Meta:
        model = Survey
        fields = '__all__'


class SurveyQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", )


class AnswerCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=UserSerializer())
    question = serializers.HiddenField(default=QuestionSerializer())
    survey = serializers.HiddenField(default=SurveySerializer())

    # user_id = serializers.ReadOnlyField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=UserSerializer())
    question = serializers.HiddenField(default=QuestionSerializer())
    survey = serializers.HiddenField(default=SurveySerializer())

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionOneFieldSerializer()
    class Meta:
        model = Answer
        fields = '__all__'


class NewAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class AnswerViewSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = '__all__'
