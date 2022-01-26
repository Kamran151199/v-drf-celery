from apps.computer.views.pearson import CorrelationViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', CorrelationViewSet)

urlpatterns = router.urls

