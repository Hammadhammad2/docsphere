from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, UpdateView

from organizations.choices import InviteStatus, Role
from organizations.forms import CreateOrganizationForm, CreateOrganizationInviteForm, UpdateOrganizationForm
from organizations.models import INVITE_EXPIRY_DAYS, Organization, OrganizationInvite, UserOrganization
from organizations.permissions import user_can_manage_org
from organizations.services import send_organization_invite_email


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    context_object_name = "organizations"
    template_name = "organizations/organization_list.html"
    login_url = reverse_lazy("login")
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        search_query = self.request.GET.get("q", "").strip()

        queryset = Organization.objects.filter(
            members=self.request.user,
        )

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = self.object
        context["members"] = (
            UserOrganization.objects.filter(organization=organization).select_related("user").order_by("user__email")
        )

        context["pending_invites"] = OrganizationInvite.objects.filter(
            organization=organization,
            status=InviteStatus.PENDING,
            expires_at__gt=timezone.now(),
        ).order_by("email")

        context["can_invite"] = user_can_manage_org(self.request.user, organization)
        return context


class OrganizationInviteCreateView(LoginRequiredMixin, FormView):
    form_class = CreateOrganizationInviteForm
    template_name = "organizations/organization_invite_create.html"
    login_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        self.organization = get_object_or_404(
            Organization.objects.filter(members=request.user),
            pk=kwargs["pk"],
        )

        if not user_can_manage_org(request.user, self.organization):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organization"] = self.organization
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organization"] = self.organization
        return context

    def form_valid(self, form):
        invite = OrganizationInvite.objects.create(
            organization=self.organization,
            email=form.cleaned_data["email"],
            invited_by=self.request.user,
            expires_at=timezone.now() + timedelta(days=INVITE_EXPIRY_DAYS),
            status=InviteStatus.PENDING,
        )

        if send_organization_invite_email(invite=invite, request=self.request):
            messages.success(self.request, f"Invite sent to {invite.email}.")
        else:
            messages.warning(
                self.request,
                f"Invite saved for {invite.email}, but the email could not be sent. "
                "Check EMAIL_* settings and the server log.",
            )

        return redirect("organizations:organization_detail", pk=self.organization.pk)


class OrganizationInviteAcceptLandingView(TemplateView):
    template_name = "organizations/invite_accept_landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invite = get_object_or_404(OrganizationInvite, token=self.kwargs["token"])
        context["invite"] = invite
        context["organization"] = invite.organization
        return context
