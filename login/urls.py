from django.urls import path
from .views import login, my_login, my_logout

urlpatterns = [
    path('login/', my_login, name="login_handler"),
    path('logout', my_logout, name="logout_handler"),
]
