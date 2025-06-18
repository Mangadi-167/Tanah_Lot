# tanah_lot/chatbot/urls.py
from django.urls import path
from . import views 

app_name = 'chatbot' 

urlpatterns = [
  
    path("", views.chat_view, name="chatbot"), 
    path("clear-history/", views.clear_chat_history, name="clear_chat"),
  
]