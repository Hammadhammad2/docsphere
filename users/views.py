from django.http import JsonResponse
from django.views import View


class LoginView(View):
    def get(self, request):
        return JsonResponse({"message": "Hello, World!"})

    def post(self, request):
        return JsonResponse({"message": "Hello, World!"})


class RegisterView(View):
    def get(self, request):
        return JsonResponse({"message": "Hello, World!"})

    def post(self, request):
        return JsonResponse({"message": "Hello, World!"})
