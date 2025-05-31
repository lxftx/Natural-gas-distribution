from django.urls import path
from gas.views import CalculateAPIView, DefaultInputValuesAPIView

app_name = 'gas'

urlpatterns = [
    path("calculate/", CalculateAPIView.as_view(), name="calculate"),
    path("default/", DefaultInputValuesAPIView.as_view(), name="default")
]