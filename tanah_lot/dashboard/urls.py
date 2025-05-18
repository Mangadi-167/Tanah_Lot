from django.urls import path

from . import views

urlpatterns = [

    # khusus article
    path("", views.index, name="article_data"),
  
    

    # khusus user
    path("users/data/", views.user, name="users_data"),
]