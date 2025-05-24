from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="history_index"),
    path("facilities/", views.facilities, name="facilities"),
    path("tickets/", views.tickets, name="tickets"),
    path("sitemaps/", views.sitemaps, name="sitemaps"),
    
]