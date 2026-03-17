from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from organizations.choices import Role
from organizations.forms.create_organization_form import CreateOrganizationForm
from organizations.forms.update_organization_form import UpdateOrganizationForm
from organizations.models import Organization, UserOrganization


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    context_object_name = "organizations"
    template_name = "organizations/organization_list.html"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Organization.objects.filter(members=self.request.user)


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
        if self.request.user.is_superuser:
            queryset = Organization.objects.all()
        else:
            queryset = Organization.objects.filter(members=self.request.user)
        return queryset


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    context_object_name = "organization"
    template_name = "organizations/organization_detail.html"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Organization.objects.filter(members=self.request.user)
