from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="article_data"),
  
    # path('detail/', views.detail, name='attractions_detail'), 
]