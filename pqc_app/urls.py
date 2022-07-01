from django.urls import path
from .views import view_cam_file, pqc_up_load

urlpatterns = [
    path('view/', view_cam_file, name="pqc_view"),
    path('load/', pqc_up_load, name="pqc_upload"),
]
