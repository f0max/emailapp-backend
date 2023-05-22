from django.db import models


class Mail(models.Model):
    subject = models.CharField(max_length=100)
    sender = models.CharField(max_length=50)
    recipient = models.CharField(max_length=50)
    body = models.CharField(max_length=300)
    status = models.CharField(max_length=30, default="sent")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
