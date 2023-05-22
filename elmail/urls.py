from django.urls import path
from .views import *


urlpatterns = [
    path('sendmail/', SendMailView.as_view(), name='sendmail'),
]