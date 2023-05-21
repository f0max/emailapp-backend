from django.urls import path
from .views import MailViewSet, SendMailView


urlpatterns = [
    path('sendmail/', SendMailView.as_view(), name='sendmail'),
]