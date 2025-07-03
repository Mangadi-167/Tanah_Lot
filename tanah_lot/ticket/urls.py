
from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [
  
    path("", views.index, name="ticket"),


    path("confirmation/<str:order_id>/", views.order_confirmation, name="order_confirmation"),

  
    path("transaction/", views.data, name="transaction_data"),
    path("transaction/detail/<str:pk>/", views.detail, name="transaction_detail"),
   
    path("midtrans-webhook/", views.midtrans_webhook, name="midtrans_webhook"),


    path("verify/<str:order_id>/", views.verify_ticket, name="verify_ticket"),
    path("resend-eticket/<str:order_id>/", views.resend_eticket, name="resend_eticket"),
]