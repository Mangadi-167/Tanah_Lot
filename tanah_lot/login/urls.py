# login/urls.py
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path("", views.index, name="login"),
    path("register/", views.register, name="register"),
   
    path("logout/", views.user_logout, name="logout"),
]