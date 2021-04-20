- Клонируем проект
- Мигрируем БД
- Запускаем локальный сервер
- Из интерфейса DRF делаем запросы

Для админа: <br>
localhost:8000/api/v1/survey_app/survey/ - список всех опросов <br>
localhost:8000/api/v1/survey_app/survey/active/ - список всех активных опросов <br>
localhost:8000/api/v1/survey_app/survey/update/(id_опроса) - редактирование опроса <br>
localhost:8000/api/v1/survey_app/survey/delete/(id_опроса) - удаление опроса <br>
localhost:8000/api/v1/survey_app/survey/detail/(id_опроса) - просмотр опроса <br>
localhost:8000/api/v1/survey_app/question/ - список всех вопросов <br>
localhost:8000/api/v1/survey_app/question/create - создание вопроса <br>
localhost:8000/api/v1/survey_app/question/update/(id_вопроса) - редактирование вопроса <br>
localhost:8000/api/v1/survey_app/question/delete/(id_вопроса) - удаление вопроса <br>

Для пользователя:
localhost:8000/api/v1/survey_app/survey/active/ - список всех активных опросов <br>
localhost:8000/api/v1/survey_app/survey/detail/(id_опроса) - просмотр опроса <br>
localhost:8000/api/v1/survey_app/answer/create/(id_вопроса) - создание ответа на вопрос <br>
localhost:8000/api/v1/survey_app/answer/my_answer/ - просмотр всех ответов для пользователя <br>

Для анонимного пользователя:
localhost:8000/api/v1/survey_app/survey/active/ - список всех активных опросов <br>
localhost:8000/api/v1/survey_app/answer/create/(id_вопроса) - создание ответа на вопрос <br>
