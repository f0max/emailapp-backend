from django.urls import path
from .views import *


urlpatterns = [
    path('sendmail/', SendMailView.as_view(), name='sendmail'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('sent/', SentView.as_view(), name='sent'),
    path('junk/', JunkView.as_view(), name='junk'),
    path('trash/', TrashView.as_view(), name='trash'),
    path('chstatus/', ChangeStatusView.as_view(), name='chstatus'),
    path('delete/', DeleteMailView.as_view(), name='deletemail')
]