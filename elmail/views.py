from smtplib import SMTP
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Mail
from .serializers import MailSerializer, SendMailSerializer
from emailapp.smtp_config import *

class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer


class SendMailView(APIView):
    def post(self, request):
            try:
                # Сериализируем данные из запроса
                data = request.data
                serializer = SendMailSerializer(data=data)

                # Проверка на соответствие с моделью
                if not serializer.is_valid():
                    return Response({
                    'data': serializer.errors,
                    'message': "Invalid request"
                }, status= status.HTTP_400_BAD_REQUEST)

                subject = data['subject']
                recipient = data['recipient']
                body = data['body']

                email_headers = f"From: {smtp_username}\nTo: {recipient}\nSubject: {subject}\n\n"
                email_message = email_headers + body

                try:
                    # Установка соединения с SMTP-сервером
                    with SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_username, smtp_password)

                        subject = data['subject']
                        recipient = data['recipient']
                        body = data['body']

                        # Создание письма
                        email_headers = f"From: {smtp_username}\nTo: {recipient}\nSubject: {subject}\n\n"
                        email_message = email_headers + body

                        # Отправка письма
                        server.sendmail(smtp_username, recipient, email_message)
                        server.quit()
                except:
                    return Response({
                        'data': {},
                        'message': "Something went wrong with smtp"
                    }, status= status.HTTP_400_BAD_REQUEST)

                # Отправленное письмо сохраниться в БД
                serializer.save()

                return Response({
                    'data': serializer.data,
                    'message': "Message successfuly sent"
                }, status= status.HTTP_201_CREATED)

            except:
                return Response({
                    'data': {},
                    'message': "Something went wrong"
                }, status= status.HTTP_400_BAD_REQUEST)
            