from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from documents.forms import DocumentCreateForm, DocumentUpdateForm
from documents.models import Document
from projects.models import Project


class AccessProjectMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.project = get_object_or_404(
            Project.objects.filter(organization__members=request.user).select_related("organization"),
            pk=kwargs["project_pk"],
        )


class DocumentListView(AccessProjectMixin, ListView):
    model = Document
    template_name = "documents/document_list.html"
    context_object_name = "documents"
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        search_query = self.request.GET.get("q", "").strip()
        queryset = Document.objects.filter(project=self.project).select_related("author")

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        return queryset.order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class DocumentDetailView(AccessProjectMixin, DetailView):
    model = Document
    template_name = "documents/document_detail.html"
    context_object_name = "document"

    def get_queryset(self):
        return Document.objects.filter(project=self.project).select_related("author", "project")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context


class DocumentCreateView(AccessProjectMixin, CreateView):
    model = Document
    form_class = DocumentCreateForm
    template_name = "documents/document_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context

    def form_valid(self, form):
        document = form.save(commit=False)
        document.project = self.project
        document.author = self.request.user
        document.save()

        return redirect(
            "documents:document_detail",
            project_pk=self.project.pk,
            pk=document.pk,
        )


class DocumentUpdateView(AccessProjectMixin, UpdateView):
    model = Document
    form_class = DocumentUpdateForm
    template_name = "documents/document_update.html"
    context_object_name = "document"

    def get_queryset(self):
        return Document.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context

    def get_success_url(self):
        return reverse(
            "documents:document_detail",
            kwargs={"project_pk": self.project.pk, "pk": self.object.pk},
        )


class DocumentDeleteView(AccessProjectMixin, DeleteView):
    model = Document
    template_name = "documents/document_confirm_delete.html"
    context_object_name = "document"

    def get_queryset(self):
        return Document.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context

    def get_success_url(self):
        return reverse("documents:list_documents", kwargs={"project_pk": self.project.pk})
