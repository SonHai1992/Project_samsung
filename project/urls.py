from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('login.urls')),
    path('cad-cam/', include('cad_cam_app.urls')),
    path('pqc/', include('pqc_app.urls')),
]+ static(settings.MEDIA_URL, documents_root=settings.MEDIA_ROOT)
