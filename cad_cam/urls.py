from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('', include('login.urls')),
    path('cad-cam/', include('cad_cam_app.urls'))
]
