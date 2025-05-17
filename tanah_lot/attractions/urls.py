from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="attractions_index"),
  
    path('detail/', views.detail, name='attractions_detail'), 
]