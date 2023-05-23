import easyimap
import poplib
import emailapp.smtp_config as cfg
from smtplib import SMTP
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SendMailSerializer
from .models import Mail
from user.models import SMTPUser
from django.core.cache import cache


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

            session = request.COOKIES.get("session_cookie")
            user = cache.get(session)
            password = SMTPUser.objects.get(login=user).password

            sender = data['sender']
            subject = data['subject']
            recipient = data['recipient']
            body = data['body']

            try:
                # Установка соединения с SMTP-сервером
                with SMTP(cfg.smtp_server, cfg.smtp_port) as server:
                    server.starttls()
                    server.login(sender, password)

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

        except Exception as err:
            print(err)
            return Response({
                'message': "Something went wrong"
            })


class InboxView(APIView):
    def get(self, request):
        try:
            session = request.COOKIES.get("session_cookie")
            user = cache.get(session)
            password = SMTPUser.objects.get(login=user).password

            server = easyimap.connect(cfg.imap_server, user, password)

            owner_id = SMTPUser.objects.get(login=user).id
            msgs = []

            for mail_id in server.listids():
                mail = server.mail(mail_id)
                msgs.append({
                    "subject": mail.title,
                    "sender": mail.from_addr,
                    "recipient": mail.to,
                    "body": mail.body,
                    "date": mail.date,
                    "status": "inbox",
                    "owner": owner_id
                })

            server.quit()

            for mail in msgs:
                serializer = SendMailSerializer(data=mail)
                if not serializer.is_valid():
                    print(serializer.errors)
                else:
                    serializer.save()

            server = poplib.POP3(cfg.imap_server)
            server.stls()
            server.user(user)
            server.pass_(password)
            num_messages = len(server.list()[1])
            for i in range(num_messages):
                server.dele(i+1)
            server.quit()

            mails = Mail.objects.filter(owner_id=owner_id, status="inbox")
            serializer = SendMailSerializer(mails, many=True)

            return Response(serializer.data)
        
        except Exception as err:
            print(err)
            return Response({
                'message': "Something went wrong"
            })
    

class SentView(APIView):
    def get(self, request):
        try:
            session = request.COOKIES.get("session_cookie")
            user = cache.get(session)
            owner_id = SMTPUser.objects.get(login=user).id
            mails = Mail.objects.filter(owner_id=owner_id, status="sent")
            serializer = SendMailSerializer(mails, many=True)

            return Response(serializer.data)
        
        except Exception as err:
            print(err)
            return Response({
                'message': "Something went wrong"
            })


class JunkView(APIView):
    def get(self, request):
        try:
            session = request.COOKIES.get("session_cookie")
            user = cache.get(session)
            owner_id = SMTPUser.objects.get(login=user).id
            mails = Mail.objects.filter(owner_id=owner_id, status="junk")
            serializer = SendMailSerializer(mails, many=True)

            return Response(serializer.data)
        
        except Exception as err:
            print(err)
            return Response({
                'message': "Something went wrong"
            })


class TrashView(APIView):
    def get(self, request):
        try:
            session = request.COOKIES.get("session_cookie")
            user = cache.get(session)
            owner_id = SMTPUser.objects.get(login=user).id
            mails = Mail.objects.filter(owner_id=owner_id, status="trash")
            serializer = SendMailSerializer(mails, many=True)

            return Response(serializer.data)
        
        except Exception as err:
            print(err)
            return Response({
                'message': "Something went wrong"
            })


class ChangeStatusView(APIView):
    def post(self, request):
        try:
            data = request.data
            if 'id' not in data:
                return Response({
                    'message': "id is required"
                })
            
            if 'status' not in data:
                return Response({
                    'message': "status is required"
                })

            try:
                mail = Mail.objects.get(id=data['id'])
                mail.status = data['status']
                mail.save()
            except:
                return Response({
                    'message': "Something went wrong. Check mail id."
                })
            
            serializer = SendMailSerializer(mail)

            return Response(serializer.data)
        
        except Exception as err:
            print(err)
            return Response({
                'message': "Something went wrong"
            })


class DeleteMailView(APIView):
    def post(self, request):
        try:
            data = request.data
            if 'id' not in data:
                return Response({
                    'message': "id is required"
                })
            
            mail = Mail.objects.get(id=data['id'])
            mail.delete()

            return Response(status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
            return Response({
                'message': "Something went wrong"
            })
