from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from users.forms.login_form import LoginForm
from users.forms.register_form import RegisterForm


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("organizations:list_organizations")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login")


# TODO: This view will not be used later as we will use the invite system to register users.
class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("organizations:list_organizations")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
