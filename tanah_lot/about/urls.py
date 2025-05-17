from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="history_index"),
    # path('artikel/<int:artikel_id>/', views.detail_artikel, name='detail_artikel'),
    #  path('news/detail-static/', views.detail_artikel_static, name='detail_artikel_static'), 
    path('detail/', views.detail, name='news_detail'), 
]