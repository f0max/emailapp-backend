from django.urls import path
from .views import *


urlpatterns = [
    path('sendmail/', SendMailView.as_view(), name='sendmail'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('test/', TestView.as_view())
]