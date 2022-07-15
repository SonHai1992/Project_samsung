from django.urls import path
from .views import index, comfirm_pqc


urlpatterns = [
    path('index', index, name="index_pqc"),
    path('comfirm/<int:id_input>', comfirm_pqc, name="comfirm"),

]
