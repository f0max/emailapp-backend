from django.urls import path
from .views import *


urlpatterns = [
    path('login/by/session/', LoginBySession.as_view(), name='loginbysession'),
    path('login/', UserAuth.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]