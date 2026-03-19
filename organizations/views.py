from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from organizations.choices import Role
from organizations.forms import CreateOrganizationForm, UpdateOrganizationForm
from organizations.models import Organization, UserOrganization


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    context_object_name = "organizations"
    template_name = "organizations/organization_list.html"
    login_url = reverse_lazy("login")
    paginate_by = settings.PAGINATE_BY

    def get_search_query(self):
        return self.request.GET.get("q", "").strip()

    def get_queryset(self):
        queryset = Organization.objects.filter(members=self.request.user)

        search_query = self.get_search_query()

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

        return queryset.order_by("-created")


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = CreateOrganizationForm
    template_name = "organizations/organization_create.html"
    success_url = reverse_lazy("organizations:list_organizations")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        organization = form.save()
        UserOrganization.objects.create(
            organization=organization,
            user=self.request.user,
            role=Role.OWNER,
        )
        return super().form_valid(form)


class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = UpdateOrganizationForm
    context_object_name = "organization"
    template_name = "organizations/organization_update.html"
    success_url = reverse_lazy("organizations:list_organizations")
    login_url = reverse_lazy("login")

    def get_queryset(self):
        user = self.request.user

        return Organization.objects.filter(Q(members=user) | Q() if user.is_superuser else Q(members=user))


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    context_object_name = "organization"
    template_name = "organizations/organization_detail.html"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Organization.objects.filter(members=self.request.user)
