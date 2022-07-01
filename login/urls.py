from django.urls import path
from .views import login, my_view, my_logout

urlpatterns = [
    # path('', login, name="login_han"),
    path('accounts/login/', my_view, name="login_handler"),
    # path('logout', my_logout, name="logout_handler"),
]
