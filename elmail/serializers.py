from rest_framework import serializers
from .models import Mail


class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = '__all__'


class SendMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mail
        fields = '__all__'