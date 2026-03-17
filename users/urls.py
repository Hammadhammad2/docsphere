from django.urls import path

from users.views import AcceptInviteView, InviteUserView, LoginView, LogoutView, RegisterView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("invite/", InviteUserView.as_view(), name="invite_user"),
    path("invite/<uuid:token>/", AcceptInviteView.as_view(), name="accept_invite"),
]
