from django.urls import path

from . import views
app_name = 'attractions'
urlpatterns = [
    path("", views.index, name="attractions_index"),
  
    path('detail/<int:pk>/', views.detail, name='attractions_detail'), 
]
