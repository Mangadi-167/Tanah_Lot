from django.urls import path

from . import views

urlpatterns = [

    # khusus dashboard
    path("", views.index, name="dashboard"),
    
    

    # khusus article
    path("article/data/", views.article, name="article_data"),
    
    path("article/add", views.addArticle, name="add_article"),



     # khusus event calender
    path("calender/data/", views.calender, name="calender_data"),
    path("calender/add/", views.addCalender, name="add_calender"),
    path("calender/edit/", views.editCalender, name="edit_calender"),
  
    

    # khusus user
    path("users/data/", views.user, name="users_data"),
    path("users/add", views.addUser, name="add_user"),


    # khusus reset password
    path("users/reset-password", views.resetPassword, name="reset_password")
]