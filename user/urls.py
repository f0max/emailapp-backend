from django.urls import path
from .views import UserByToken


urlpatterns = [
    path('user/by/token/', UserByToken.as_view()),
]