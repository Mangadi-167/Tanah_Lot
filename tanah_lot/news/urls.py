from django.urls import path

from . import views

app_name = 'news' 

urlpatterns = [
    path("", views.index, name="news_index"),
  
     path('detail/<int:pk>/', views.detail, name='news_detail'), 
]