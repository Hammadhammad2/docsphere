from django.urls import path

from organizations.views import (
    OrganizationCreateView,
    OrganizationDetailView,
    OrganizationListView,
    OrganizationUpdateView,
)

app_name = "organizations"

urlpatterns = [
    path("", OrganizationListView.as_view(), name="list_organizations"),
    path("<uuid:id>/", OrganizationDetailView.as_view(), name="detail_organization"),
    path("create/", OrganizationCreateView.as_view(), name="create_organization"),
    path("update/<uuid:id>/", OrganizationUpdateView.as_view(), name="update_organization"),
]
