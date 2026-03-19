from django.urls import path

from organizations import views

urlpatterns = [
    path("", views.OrganizationListView.as_view(), name="list_organizations"),
    path("<int:id>/", views.OrganizationDetailView.as_view(), name="organization_detail"),
    path("create/", views.OrganizationCreateView.as_view(), name="create_organization"),
    path("<int:id>/update/", views.OrganizationUpdateView.as_view(), name="update_organization"),
]
