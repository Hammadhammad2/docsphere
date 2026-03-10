from django.urls import path

from organizations import views

app_name = "organizations"

urlpatterns = [
    path("", views.organization_list, name="list"),
    path("<uuid:id>/", views.organization_detail, name="detail"),
    path("create/", views.organization_create, name="create"),
    path("update/<uuid:id>/", views.organization_update, name="update"),
]