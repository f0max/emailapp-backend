from rest_framework import serializers
from .models import SMTPUser


class SMTPUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SMTPUser
        fields = '__all__'
