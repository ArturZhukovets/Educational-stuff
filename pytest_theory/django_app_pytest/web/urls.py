from django.urls import path
from . import views

app_name = 'web'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('log-up/', views.CreateUserView.as_view(), name='log_up'),
]

