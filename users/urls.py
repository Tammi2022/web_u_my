from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from users.views import UserLoginView, UserRegisterView, UsersListView, UsersDetailsView

urlpatterns = [
    path('login', csrf_exempt(UserLoginView.as_view())),
    path('register', csrf_exempt(UserRegisterView.as_view())),
    path('list', csrf_exempt(UsersListView.as_view())),
    path('<int:id>', csrf_exempt(UsersDetailsView.as_view())),
]
