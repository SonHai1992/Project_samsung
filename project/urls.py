from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('login.urls')),
    path('cad-cam/', include('cad_cam_app.urls')),
    path('pqc/', include('pqc_app.urls')),
]
