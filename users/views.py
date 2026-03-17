import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import FormView

from organizations.choices import InviteStatus, Role
from organizations.models import INVITE_EXPIRY_DAYS, Invite, UserOrganization
from users.forms.invite_form import InviteForm
from users.forms.login_form import LoginForm
from users.models import User


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("organizations:list_organizations")

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        return next_url if next_url else str(self.success_url)

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login")


class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        user = User.objects.create_user(email=email, password=password)

        login(request, user)
        return JsonResponse({"message": "User created successfully"})


class InviteUserView(FormView):
    template_name = "users/invite_user.html"
    form_class = InviteForm
    success_url = reverse_lazy("invite_user")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_organizations"] = self.request.user.user_organizations.exists()
        return context

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        organization = form.cleaned_data["organization"]

        if Invite.objects.filter(email=email, organization=organization, status=InviteStatus.PENDING).exists():
            form.add_error("email", "This user is already invited to this organization.")
            return self.form_invalid(form)

        if organization.user_organizations.filter(user__email=email).exists():
            form.add_error("email", "This user is already a member.")
            return self.form_invalid(form)

        expires_at = timezone.now() + timedelta(days=INVITE_EXPIRY_DAYS)
        Invite.objects.create(
            email=email,
            organization=organization,
            invited_by=self.request.user,
            expires_at=expires_at,
        )
        messages.success(self.request, f"Invite sent to {email}.")
        return redirect(self.get_success_url())


class AcceptInviteView(View):
    template_name = "users/invite_accept.html"

    def get(self, request, token):
        invite = get_object_or_404(Invite, token=token)
        context = self._get_context(invite)
        return self._render(request, context)

    def post(self, request, token):
        invite = get_object_or_404(Invite, token=token)
        if not request.user.is_authenticated:
            return redirect("login")
        if request.POST.get("action") == "decline":
            messages.info(request, "Invite declined.")
            return redirect("organizations:list_organizations")

        context = self._validate_accept(request, invite)
        if context.get("error"):
            return self._render(request, context)

        UserOrganization.objects.get_or_create(
            user=request.user, organization=invite.organization, defaults={"role": Role.MEMBER}
        )
        invite.status = InviteStatus.ACCEPTED
        invite.save(update_fields=["status", "modified"])
        messages.success(request, f"You joined {invite.organization.name}.")
        return redirect("organizations:list_organizations")

    def _get_context(self, invite):
        if invite.status != InviteStatus.PENDING:
            return {
                "error": "already_handled",
                "message": "This invite was already used or declined.",
                "invite": invite,
            }
        if timezone.now() >= invite.expires_at:
            return {"error": "expired", "message": "This invite has expired.", "invite": invite}
        return {
            "invite": invite,
            "organization_name": invite.organization.name,
            "inviter_email": invite.invited_by.email,
            "expires_at": invite.expires_at,
        }

    def _validate_accept(self, request, invite):
        ctx = self._get_context(invite)
        if ctx.get("error"):
            return ctx
        if request.user.email != invite.email:
            return {
                "error": "wrong_user",
                "message": "This invite was sent to a different email address.",
                "invite": invite,
                **ctx,
            }
        if invite.organization.user_organizations.filter(user=request.user).exists():
            return {
                "error": "already_member",
                "message": "You are already a member of this organization.",
                "invite": invite,
                **ctx,
            }
        return ctx

    def _render(self, request, context):
        return render(request, self.template_name, context)
