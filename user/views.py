import uuid
import imaplib
from emailapp.smtp_config import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SMTPUserSerializer
from django.core.cache import cache


class LoginBySession(APIView):
    def get(self, request):
        # Получаем сессию из куки из запроса
        session = request.COOKIES.get("session_cookie")

        # Ищем пользователя по сессии в redis
        user = cache.get(session)

        return Response({
            'user': user
        }, status=status.HTTP_200_OK)
    

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
            imap = imaplib.IMAP4_SSL(imap_server)

            # Проверка авторизации
            try:
                imap.login(login, passwd)
            except:
                return Response({
                    'message': "Authentication failed."
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Создание сессии для пользователя
            session = str(uuid.uuid4())

            # Сохраняем пару session:login в redis на 1 час
            cache.set(session, login, timeout=3600)

            response = Response({
                'session': session,
                'message': "Authentication success."
            }, status=status.HTTP_200_OK)

            # Сохраняем сессию в куке
            response.set_cookie("session_cookie", session)

            return response

        except:
            return Response({
                    'message': "Something went wrong"
                }, status= status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def get(self, request):
        # Получаем сессию из куки из запроса
        session = request.COOKIES.get("session_cookie")

        # Удаляем сессию из redis
        cache.delete(session)

        return Response(status=status.HTTP_200_OK)