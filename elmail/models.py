from django.db import models
from user.models import SMTPUser


class Mail(models.Model):
    subject = models.CharField(max_length=500)
    sender = models.CharField(max_length=500)
    recipient = models.CharField(max_length=500)
    body = models.CharField(max_length=5000)
    status = models.CharField(max_length=30, default="sent")
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(SMTPUser, models.DO_NOTHING, db_column='owner_id')

    def __str__(self):
        return self.subject
