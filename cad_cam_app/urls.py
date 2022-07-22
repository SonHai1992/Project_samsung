from django.urls import path
from .views import view_pqc_result, cam_up_load, index, Delete, Edit_upload, Search

urlpatterns = [
    path('view/<int:id_input>', view_pqc_result, name="view_pqc_result"),
    path('load/', cam_up_load, name="cam_upload"),
    path('delete/<int:id_input>', Delete, name="deleted"),
    path('edit/<int:id_input>', Edit_upload, name="edit"),
    path('search/', Search, name="search"),
    path('', index, name="index"),
]
