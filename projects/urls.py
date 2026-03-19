from django.urls import path

from projects.views import ProjectCreateView, ProjectDetailView, ProjectListView, ProjectUpdateView

app_name = "projects"

urlpatterns = [
    path("", ProjectListView.as_view(), name="list_projects"),
    path("create/<int:organization_pk>/", ProjectCreateView.as_view(), name="create_project"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("<int:pk>/update/", ProjectUpdateView.as_view(), name="update_project"),
]
