from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="ticket"),
    path("transaction/", views.data, name="transaction_data"),
]