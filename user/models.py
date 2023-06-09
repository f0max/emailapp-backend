from django.db import models


class SMTPUser(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50, default="")
    surname = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.login
