from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from organizations.models import Organization
from projects.forms import ProjectCreateForm, ProjectUpdateForm
from projects.models import Project


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = settings.PAGINATE_BY
    login_url = reverse_lazy("login")

    def get_queryset(self):
        search_query = self.request.GET.get("q", "").strip()

        queryset = Project.objects.filter(organization__members=self.request.user).select_related(
            "organization",
        )

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query),
            )
        return queryset.order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Project.objects.filter(organization__members=self.request.user).select_related("organization")


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "projects/project_create.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("projects:list_projects")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.organization = get_object_or_404(
            Organization.objects.filter(members=request.user),
            pk=kwargs["organization_pk"],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organization"] = self.organization
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.organization = self.organization
        project.save()
        return redirect(self.success_url)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = "projects/project_update.html"
    context_object_name = "project"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Project.objects.filter(organization__members=self.request.user)

    def get_success_url(self):
        return reverse("projects:project_detail", kwargs={"pk": self.object.pk})
