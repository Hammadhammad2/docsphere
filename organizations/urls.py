from django.urls import path

from organizations import views

app_name = "organizations"

urlpatterns = [
    path("", views.organization_list, name="list_organizations"),
    path("<uuid:id>/", views.organization_detail, name="detail_organization"),
    path("create/", views.organization_create, name="create_organization"),
    path("update/<uuid:id>/", views.organization_update, name="update_organization"),
]
