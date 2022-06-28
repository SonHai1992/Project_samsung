from django.urls import path
from .views import view_page

urlpatterns = [
    path('', view_page, name="cad_cam_view"),
]
