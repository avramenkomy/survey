from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveAPIView
from datetime import datetime
from .permissions import IsOwner, IsOwnerOrReadOnly, ReadOnly


class UserAllView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()

    def get(self, request):
        print(User.objects.all())
        # qs = Answer.objects.filter(user_id=request.user.id)
        data = UserSerializer(User.objects.all(), many=True).data
        # return Response({"String with some data"}, status=status.HTTP_200_OK)
        return Response(data=data, status=status.HTTP_200_OK)


class SurveyAllView(ListAPIView):
    serializer_class = SurveyQuestionsSerializer
    queryset = Survey.objects.all()
    permission_classes = (IsAdminUser,)


class SurveyActiveView(ListAPIView):
    serializer_class = SurveySerializer
    queryset = Survey.objects.filter(start_date__lte=datetime.now(), end_date__gt=datetime.now())


class SurveyCreateView(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SurveySerializer


class SurveyUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()


class SurveyDeleteView(RetrieveDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()


class SurveyDetailView(RetrieveAPIView):
    queryset = Survey.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SurveySerializer


class QuestionView(ListAPIView):
    queryset = Question.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = QuestionSerializer


class QuestionCreateView(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = QuestionSerializer


class QuestionUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionDeleteView(RetrieveDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerCreateView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswerCreateSerializer

    def get(self, request, pk):
        if Answer.objects.all().filter(question__id=pk).filter(user_id=request.user.id):
            return Response({"Answer is already exists. Please entry update you answer with answer/update/<int:pk>"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(QuestionSerializer(Question.objects.get(pk=pk)).data)

    def post(self, request, pk):
        if (Answer.objects.filter(question__id=pk).filter(user_id=request.user.id)):
            return Response({"Answer is already exists. Please entry update you answer with answer/update/<int:pk>"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        question = Question.objects.get(pk=pk)
        if user.is_authenticated:
            user_id = user.id
            survey = question.survey
            question_id = question.id
            answer_text = request.data['answer_text']
            data = {
                "user_id": user_id,
                "survey": survey.id,
                "question": question_id,
                "answer_text": answer_text,
            }
            serializer = AnswerSerializer(data=data)
            if serializer.is_valid():
                answer = serializer.save()
                return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            token = request.headers["Cookie"].split('=')[1].split(';')[0]
            data = {
                "user_id": token,
                "survey": question.survey.id,
                "question": question.id,
                "answer_text": request.data['answer_text']
            }
            if (AnonymousUser.objects.filter(token=token)):
                if (Answer.objects.filter(question__id=pk).filter(user_id=token)):
                    return Response({"Answer is already exists. Please entry update you answer with answer/update/<int:pk>"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = AnswerSerializer(data=data)
                    if serializer.is_valid():
                        answer = serializer.save()
                        return Response(AnswerSerializer(answer).data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                newAnonymous = AnonymousUser(token=token)
                newAnonymous.save()
                serializer = AnswerSerializer(data=data)
                if serializer.is_valid():
                    answer = serializer.save()
                    return Response(AnswerSerializer(answer).data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"anonymous user answer"}, status=status.HTTP_200_OK)



# get all answers by user
class AnswerView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AnswerViewSerializer

    def get(self, request, pk):
        qs = Answer.objects.all().filter(user_id=pk)  # .order_by('survey')
        return Response(AnswerSerializer(qs, many=True).data, status=status.HTTP_200_OK)


class AnswerWithSurvey(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk_user, pk_survey):
        qs = Answer.objects.all().filter(user_id=pk_user).filter(survey=pk_survey)
        print(qs.first().user_id)
        if request.user.id == qs.first().user_id:
            return Response(AnswerSerializer(qs, many=True).data, status=status.HTTP_200_OK)
        return Response({"Вы не можете просматривать этот список"}, status=status.HTTP_400_BAD_REQUEST)


class AnswerByUserView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        if request.user.is_authenticated:
            qs = Answer.objects.filter(user_id=request.user.id).order_by('survey')
            return Response(AnswerSerializer(qs, many=True).data, status=status.HTTP_200_OK)
