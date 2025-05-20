from django.urls import path

from . import views

urlpatterns = [

    # khusus article
    path("", views.index, name="article_data"),
    
    path("article/add", views.addArticle, name="add_article"),
  
    

    # khusus user
    path("users/data/", views.user, name="users_data"),
    path("users/data/add", views.addUser, name="add_user"),


    # khusus reset password
    path("users/reset-password", views.resetPassword, name="reset_password")
]