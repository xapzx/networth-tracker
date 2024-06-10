from django.urls import path

from . import apis

urlpatterns = [
    path("register/", apis.RegisterView.as_view(), name="register"),
]
