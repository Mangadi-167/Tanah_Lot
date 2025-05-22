
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("news/", include("news.urls")),
    path("attractions/", include("attractions.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("about/", include("about.urls")),
    path("login/", include("login.urls")),
    path('', views.index,name='/'),
    path("calender/", views.calender, name='calender'),
]
