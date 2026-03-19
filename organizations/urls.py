from django.urls import path

from organizations.views import (
    OrganizationCreateView,
    OrganizationDetailView,
    OrganizationInviteAcceptLandingView,
    OrganizationInviteCreateView,
    OrganizationListView,
    OrganizationUpdateView,
)

app_name = "organizations"

urlpatterns = [
    path("", OrganizationListView.as_view(), name="list_organizations"),
    path(
        "invites/accept/<str:token>/",
        OrganizationInviteAcceptLandingView.as_view(),
        name="accept_invite",
    ),
    path("<int:pk>/", OrganizationDetailView.as_view(), name="organization_detail"),
    path("create/", OrganizationCreateView.as_view(), name="create_organization"),
    path("<int:pk>/update/", OrganizationUpdateView.as_view(), name="update_organization"),
    path("<int:pk>/invite/", OrganizationInviteCreateView.as_view(), name="invite_user"),
]
