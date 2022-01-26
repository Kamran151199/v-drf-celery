from rest_framework import routers

from apps.users.views.user import UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = router.urls
