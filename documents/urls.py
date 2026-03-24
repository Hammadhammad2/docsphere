from django.urls import path

from documents.views import (
    DocumentCreateView,
    DocumentDeleteView,
    DocumentDetailView,
    DocumentListView,
    DocumentUpdateView,
)

app_name = "documents"

urlpatterns = [
    path("", DocumentListView.as_view(), name="list_documents"),
    path("create/", DocumentCreateView.as_view(), name="create_document"),
    path("<int:pk>/", DocumentDetailView.as_view(), name="document_detail"),
    path("<int:pk>/update/", DocumentUpdateView.as_view(), name="update_document"),
    path("<int:pk>/delete/", DocumentDeleteView.as_view(), name="delete_document"),
]
