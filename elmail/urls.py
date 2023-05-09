from rest_framework import routers
from .views import MailViewSet


router = routers.DefaultRouter()
router.register('list/mail', MailViewSet, 'mail')


urlpatterns = router.urls
