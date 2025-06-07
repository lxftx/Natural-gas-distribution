from django.urls import path
from user.views import (LoginAPIView, LogoutAPIView, RefreshAPIView,
                        RegisterAPIView, UserAPIView)

app_name = "user"

urlpatterns = [
    path("info/", UserAPIView.as_view(), name="information"),
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshAPIView.as_view(), name='token_refresh'),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]