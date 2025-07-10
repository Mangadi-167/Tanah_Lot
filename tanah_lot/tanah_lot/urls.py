from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from . import views as project_views
from dashboard import views as dashboard_views

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
    path('', project_views.index,name='/'),
    
    path('pakendungan/', project_views.pakendungan, name='pakendungan'),
    path('penataranmadya/', project_views.penataranmadya, name='penataranmadya'),
    path('jrokandang/', project_views.jrokandang, name='jrokandang'),
    path('njunggaluh/', project_views.njunggaluh, name='njunggaluh'),
    path('batubolong/', project_views.batubolong, name='batubolong'),
    path('batumejan/', project_views.batumejan, name='batumejan'),

    path("calender/", dashboard_views.calender_data, name='calender'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.append(
    re_path(r'^.*$', project_views.custom_404_view, name='404_catch_all')
)