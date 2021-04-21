from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveAPIView
from datetime import datetime
from django.db.models import Q
from django.http import Http404
from .permissions import IsOwner, IsOwnerOrReadOnly, ReadOnly


def is_owner(answer, user_id):
    str(user_id)
    print(type(answer.user_id), type(user_id))
    if answer.user_id != user_id:
        return False
    return True


class UserAllView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()

    def get(self, request):
        data = UserSerializer(User.objects.all(), many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


class SurveyAllView(ListAPIView):
    serializer_class = SurveyQuestionsSerializer
    queryset = Survey.objects.all()
    permission_classes = (IsAdminUser,)


class SurveyActiveView(ListAPIView):
    serializer_class = SurveyActiveSerializer
    queryset = Survey.objects.filter(start_date__lte=datetime.now(), end_date__gt=datetime.now())


class SurveyCreateView(CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SurveySerializer


class SurveyUpdateView(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SurveyUpdateSerializer
    queryset = Survey.objects.all()


class SurveyDeleteView(RetrieveDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()


class SurveyDetailView(RetrieveAPIView):
    queryset = Survey.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SurveyActiveSerializer


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
        user = request.user
        if user.is_authenticated:
            answer = Answer.objects.all().filter(question__id=pk).filter(user_id=request.user.id)
            if answer:
                return Response(
                    {"Answer is already exists. Please entry update you answer with answer/update/<int:pk>"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                question = Question.objects.get(pk=pk)
                return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)
            except Question.DoesNotExist:
                raise Http404()
        else:
            token = request.headers["Cookie"].split('=')[1].split(';')[0]
            answer = Answer.objects.all().filter(question__id=pk).filter(user_id=token)
            if answer:
                return Response(
                    {
                        "Answer is already exists. Please entry update you answer with api/v1/survey_app/answer/update/{}".format(
                            answer.first().id)},
                    status=status.HTTP_400_BAD_REQUEST)
            try:
                question = Question.objects.get(pk=pk)
                return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)
            except Question.DoesNotExist:
                raise Http404()

    def post(self, request, pk):

        user = request.user
        question = Question.objects.get(pk=pk)

        if user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = request.headers["Cookie"].split('=')[1].split(';')[0]
            anonymous = AnonymousUser.objects.filter(token=user_id)

            if len(anonymous) == 0:
                newAnonymous = AnonymousUser(token=user_id)
                newAnonymous.save()

        answer = Answer.objects.filter(Q(question__id=pk) & Q(user_id=user_id))
        if answer:
            return Response(
                {"Answer is already exists. Please entry update you answer with answer/update/{}".format(pk)},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "user_id": user_id,
            "survey": question.survey.id,
            "question": question.id,
            "answer_text": request.data['answer_text'],
        }
        serializer = NewAnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Answer is successfully created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerUpdateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AnswerUpdateSerializer

    def get(self, request, pk):
        user = request.user
        answer = Answer.objects.filter(id=pk).first()
        if answer is None:
            return Response({"Data is not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_authenticated:
            if is_owner(answer, str(request.user.id)):
                return Response(AnswerSerializer(answer).data, status=status.HTTP_200_OK)
            else:
                return Response({"You are not owner of this answer"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            token = request.headers["Cookie"].split('=')[1].split(';')[0]
            print(answer.user_id, token)
            if is_owner(answer, token):
                return Response(AnswerSerializer(answer).data, status=status.HTTP_200_OK)
            else:
                return Response({"You are not owner of this answer"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        answer = Answer.objects.filter(id=pk).first()
        if answer is None:
            return Response({"Answer is not found"}, status=status.HTTP_404_NOT_FOUND)
        if user.is_authenticated:
            if is_owner(answer, str(request.user.id)):
                answer_text = request.data['answer_text']
                answer.answer_text = answer_text
                answer.save()
                return Response(AnswerSerializer(answer).data, status=status.HTTP_200_OK)
            else:
                return Response({"You are is now owner of this answer"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Для анонима вытаскиваем токен
            token = request.headers["Cookie"].split('=')[1].split(';')[0]
            # Проверяем владельца ответа и сохраняем новый ответ
            if is_owner(answer, token):
                answer_text = request.data['answer_text']
                answer.answer_text = answer_text
                answer.save()
                return Response(AnswerSerializer(answer).data, status=status.HTTP_200_OK)
            else:
                return Response({"You are not owner of this answer"}, status=status.HTTP_400_BAD_REQUEST)


class AnswerUpdate(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnswerUpdateSerializer

    def get(self, request, pk):
        user = request.user
        if user.is_authenticated:
            user_id = str(request.user.id)
        else:
            user_id = request.headers["Cookie"].split('=')[1].split(';')[0]

        answer = Answer.objects.filter(Q(question__id=pk) & Q(user_id=request.user.id)).first()
        if answer is None:
            return Response({"Answer does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if is_owner(answer, user_id):
            return Response(AnswerSerializer(answer).data, status=status.HTTP_200_OK)
        return Response({"You are is no owner of this answer"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        user = request.user
        if user.is_authenticated:
            user_id = str(request.user.id)
        else:
            user_id = request.headers["Cookie"].split('=')[1].split(';')[0]

        answer = Answer.objects.filter(Q(question__id=pk) & Q(user_id=user_id)).first()
        if answer is None:
            return Response({"Answer does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if is_owner(answer, user_id):
            answer.answer_text = request.data["answer_text"]
            answer.save()
            return Response({"Answer is successfully updated"}, status=status.HTTP_200_OK)
        return Response({"You are is no owner of this answer"}, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = request.headers["Cookie"].split('=')[1].split(';')[0]

        qs = Answer.objects.filter(user_id=user_id).order_by('survey')
        return Response(AnswerSerializer(qs, many=True).data, status=status.HTTP_200_OK)
