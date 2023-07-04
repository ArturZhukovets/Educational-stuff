from django.urls import path
from . import views

appname = "task1"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home")
]

