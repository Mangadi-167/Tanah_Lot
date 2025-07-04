from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    
    path("admin/", admin.site.urls),
    path("ticket/", include("ticket.urls")),
    path("news/", include("news.urls")),
    path("attractions/", include("attractions.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("about/", include("about.urls")),
    path("login/", include("login.urls")),
    path("chatbot/", include("chatbot.urls")),
    path('', views.index,name='/'),
    
    path('pakendungan/', views.pakendungan,name='pakendungan'),
    path('penataranmadya/', views.penataranmadya,name='penataranmadya'),
    path('jrokandang/', views.jrokandang,name='jrokandang'),
    path('njunggaluh/', views.njunggaluh,name='njunggaluh'),
    path('batubolong/', views.batubolong,name='batubolong'),
    path('batumejan/', views.batumejan,name='batumejan'),

    path("calender/", views.calender, name='calender'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
