from django.urls import path
from gas.views import (CalculateAPIView, DefaultInputValuesAPIView,
                       HistoryAPIView)

app_name = 'gas'

urlpatterns = [
    path("calculate/", CalculateAPIView.as_view(), name="calculate"),
    path("default/", DefaultInputValuesAPIView.as_view(), name="default"),
    path("history/", HistoryAPIView.as_view(), name="history"),
]