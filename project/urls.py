from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    # path('', include('login.urls')),
    path('cad-cam/', include('cad_cam_app.urls')),
    path('pqc/', include('pqc_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
