import uuid
import imaplib
import mysql.connector
import emailapp.smtp_config as cfg
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SMTPUserSerializer
from .models import SMTPUser
from django.core.cache import cache


class LoginBySession(APIView):
    def get(self, request):
        try:
            # Получаем сессию из куки из запроса
            session = request.COOKIES.get("session_cookie")

            # Ищем пользователя по сессии в redis
            user = cache.get(session)

            return Response({
                'user': user
            }, status=status.HTTP_200_OK)
        
        except Exception as err:
            print(err)
            return Response({
                'message': "Something went wrong"
            })
    

class UserAuth(APIView):
    def post(self, request):
        try:
            # Сериализируем данные из запроса
            data = request.data
            serializer = SMTPUserSerializer(data=data)
            
            # Проверка на соответствие с моделью
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Invalid request"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            login = data['login']
            passwd = data['password']

            # Установка соединения с IMAP-сервером
            imap = imaplib.IMAP4_SSL(cfg.imap_server)

            # Проверка авторизации
            try:
                imap.login(login, passwd)
            except:
                return Response({
                    'message': "Authentication failed."
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            imap.logout()
            
            # Создание сессии для пользователя
            session = str(uuid.uuid4())

            # Сохраняем пару session:login в redis на 1 час
            cache.set(session, login, timeout=3600)

            # id пользователя
            id = SMTPUser.objects.get(login=login).id

            response = Response({
                'session': session,
                'user_id': id,
                'message': "Authentication success."
            }, status=status.HTTP_200_OK)

            # Сохраняем сессию в куке
            response.set_cookie("session_cookie", session)

            return response

        except Exception as err:
            print(err)
            return Response({
                    'message': "Something went wrong"
            })


class Logout(APIView):
    def get(self, request):
        try:
            # Получаем сессию из куки из запроса
            session = request.COOKIES.get("session_cookie")

            # Удаляем сессию из redis
            cache.delete(session)

            # Удаляем куку
            response = Response(status=status.HTTP_200_OK, data="{\"status\": \"successfully logged out\"}")
            response.delete_cookie("session_cookie")

            return response
        
        except Exception as err:
            print(err)
            return Response({
                'message': "Something went wrong"
            })
    

class Signup(APIView):
    def post(self, request):
        try:
            # Сериализируем данные из запроса
            data = request.data
            serializer = SMTPUserSerializer(data=data)

            # Проверка на соответствие с моделью
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Invalid request"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Параметры подключения к базе данных
            config = {
                'user': cfg.editor_user,
                'password': cfg.editor_password,
                'host': cfg.editor_host,
                'database': cfg.editor_db,
            }

            # Установка соединения с базой данных
            try:
                conn = mysql.connector.connect(**config)
            except:
                return Response({
                    'message': "Something went wrong with DB connection"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Создание объекта курсора
            cursor = conn.cursor()

            # INSERT-запрос
            insert_query = """
                INSERT INTO `mailbox` (`username`, `password`, `name`, `maildir`, `domain`)
                VALUES (%s, %s, %s, %s, %s)
            """

            # Подготовка данных из запроса
            username = data['login']
            password = "{PLAIN}" + data['password']

            if 'surname' not in data:
                surname = ""
            else:
                surname = data['surname']
            
            if 'name' not in data:
                name = ""
            else:
                name = data['name']

            qr_name = f"{name} {surname}"
            user_wo_domain = username.replace("@danilaovchinnikov.ru", "")
            maildir = f"danilaovchinnikov.ru/{user_wo_domain}/"
            domain = "danilaovchinnikov.ru"

            # Данные для запроса
            query_data = (username, password, qr_name, maildir, domain)

            try:
                # Выполнение INSERT-запроса
                cursor.execute(insert_query, query_data)

                # Фиксация изменений в базе данных
                conn.commit()
            # Обработка возможных ошибок
            except Exception as err:
                print(err)
                conn.rollback()
                return Response({
                    'message': "Request execution error:"
                })

            # Закрытие курсора и соединения с базой данных
            cursor.close()
            conn.close()

            serializer.save()

            return Response({
                'message': "Registration success"
            })

        except Exception as err:
            print(err)
            return Response({
                    'message': "Something went wrong"
            })
