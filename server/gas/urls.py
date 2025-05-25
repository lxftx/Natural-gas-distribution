from django.urls import path
from gas.views import CalculateAPIView

app_name = 'gas'

urlpatterns = [
    path("calculate/", CalculateAPIView.as_view(), name="calculate"),
]