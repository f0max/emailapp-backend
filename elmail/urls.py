from rest_framework import routers
from .api import MailViewSet


router = routers.DefaultRouter()
router.register('api/mail', MailViewSet, 'mail')


urlpatterns = router.urls
