import json

from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from users.forms.login_form import LoginForm
from users.models import User


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("organizations:list_organizations")

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
