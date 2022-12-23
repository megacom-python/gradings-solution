from django.urls import path
from students import views

urlpatterns = [
    path(
        "register-user/",
        views.RegisterUserAPIView.as_view(),
        name="register_user"
    ),
    path(
        "obtain-token/",
        views.ObtainTokenAPIView.as_view(),
        name="obtain_token"
    ),
]
