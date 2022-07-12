from django.urls import path
from .views import view_cam_result, cam_up_load, Updateimg, index

urlpatterns = [
    path('view/', view_cam_result, name="cad_cam_view"),
    path('load/', cam_up_load, name="cam_upload"),
    path('update/<int:id_input>', Updateimg, name="cam_update"),
    path('', index, name="index"),
]
