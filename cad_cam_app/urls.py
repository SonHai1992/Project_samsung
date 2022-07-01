from django.urls import path
from .views import view_cam_result, cam_up_load

urlpatterns = [
    path('view/', view_cam_result, name="cad_cam_view"),
    path('load/', cam_up_load, name="cam_upload"),
]
