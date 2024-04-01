from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from users.views import UserLoginView, UserRegisterView

urlpatterns = [
    # path('bc', csrf_exempt(ExportBCOrderView.as_view())),
    path('login', csrf_exempt(UserLoginView.as_view())),
    path('register', csrf_exempt(UserRegisterView.as_view())),
]