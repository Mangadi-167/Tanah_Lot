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
    path("calender/", views.calender_data, name="calender_data"),
    path("calender/add/", views.add_calender, name="add_calender"),
    # URL BARU UNTUK API
    path("api/calender/events/", views.calender_events_api, name="calender_events_api"), 
    path("calender/edit/<int:event_id>/", views.edit_calender, name="edit_calender"),
    path("calender/delete/<int:event_id>/", views.delete_calender, name="delete_calender"),
  
    

   # khusus user
    path("users/data/", views.user, name="users_data"),
    path("users/data/add", views.addUser, name="add_user"),
    path("users/data/edit/<int:pk>/", views.update_user, name="update_user"),
    path("users/data/delete/<int:pk>/", views.delete_user, name="delete_user"),
    


    # khusus reset password
    path("reset-password/", views.resetPassword, name="reset_password"),


    path("ticket-prices/", views.manage_ticket_prices, name="manage_ticket_prices"),

]