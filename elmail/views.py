from smtplib import SMTP
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SendMailSerializer
import emailapp.smtp_config  as cfg


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

            try:
                # Установка соединения с SMTP-сервером
                with SMTP(cfg.smtp_server, cfg.smtp_port) as server:
                    server.starttls()
                    server.login(cfg.smtp_username, cfg.smtp_password)

                    sender = data['sender']
                    subject = data['subject']
                    recipient = data['recipient']
                    body = data['body']

                    # Создание письма
                    email_headers = f"From: {sender}\nTo: {recipient}\nSubject: {subject}\n\n"
                    email_message = email_headers + body

                    # Отправка письма
                    server.sendmail(sender, recipient, email_message)
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
