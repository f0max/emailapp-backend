from .models import Mail
from rest_framework import viewsets
from .serializers import MailSerializer


class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
