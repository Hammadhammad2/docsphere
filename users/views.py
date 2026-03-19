from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import FormView

from users.forms import LoginForm, RegisterForm


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("organizations:list_organizations")

    def get_initial(self):
        initial = super().get_initial()
        email = (self.request.GET.get("email") or "").strip()
        if email:
            initial["email"] = email
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        next_url = (self.request.POST.get("next") or self.request.GET.get("next") or "").strip()
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return str(self.success_url)

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login")


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("organizations:list_organizations")

    def get_initial(self):
        initial = super().get_initial()
        email = (self.request.GET.get("email") or "").strip()
        if email:
            initial["email"] = email
        return initial

    def get_success_url(self):
        next_url = (self.request.POST.get("next") or self.request.GET.get("next") or "").strip()
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return str(self.success_url)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
