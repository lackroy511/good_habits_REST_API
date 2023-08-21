from django.urls import path

from users.apps import UsersConfig
from users.views import (MyTokenObtainPairView, UserActivateAPIView,
                         UserCreateAPIView)

app_name = UsersConfig.name


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(),  name='register'),
    path('activate/<str:token>/',
         UserActivateAPIView.as_view(), name='activate'),
    path('token/', MyTokenObtainPairView.as_view(),  name='get_token'),
]
