from django.urls import path
from user.views import (LoginAPIView, LogoutAPIView, RefreshAPIView,
                        RegisterAPIView)

app_name = "user"

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshAPIView.as_view(), name='token_refresh'),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]