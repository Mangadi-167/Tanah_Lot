from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [

    # khusus dashboard
    path("", views.index, name="dashboard"),
    
    

    # khusus article
    path("article/data/", views.article, name="article_data"),
    path("article/add/", views.addArticle, name="add_article"),
    path("article/update/<int:pk>/", views.update_content, name="update_content"),
    path("content/delete/<int:pk>/", views.delete_content, name="delete_content"),



     # khusus event calender
    path("calender/data/", views.calender, name="calender_data"),
    path("calender/add/", views.addCalender, name="add_calender"),
    path("calender/edit/", views.editCalender, name="edit_calender"),
  
    

   # khusus user
    path("users/data/", views.user, name="users_data"),
    path("users/data/add", views.addUser, name="add_user"),
    path("users/data/edit/<int:pk>/", views.update_user, name="update_user"),
    path("users/data/delete/<int:pk>/", views.delete_user, name="delete_user"),
    


    # khusus reset password
    path("reset-password/", views.resetPassword, name="reset_password"),

]