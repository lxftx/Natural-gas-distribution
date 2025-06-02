from django.urls import path
from rest_framework.routers import DefaultRouter

from gas.views import (CalculateAPIView, DefaultInputValuesAPIView,
                       HistoryViewSet)

app_name = 'gas'

router = DefaultRouter()
router.register(r'history', HistoryViewSet)


urlpatterns = [
    path("calculate/", CalculateAPIView.as_view(), name="calculate"),
    path("default/", DefaultInputValuesAPIView.as_view(), name="default")
] + router.urls