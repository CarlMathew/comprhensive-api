from django.urls import path
from . import views


urlpatterns = [
    path("create_users/", views.CreateUserAPI.as_view()),
    path("token/", views.CustomTokenObtainPairView.as_view())
]
