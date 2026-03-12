import json
from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from config.views import ApiView
from users.models import User


class LoginView(ApiView):
    def post(self, request):
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=HTTPStatus.UNAUTHORIZED)


class LogoutView(ApiView):
    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'})


class RegisterView(ApiView):
    def post(self, request):
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        user = User.objects.create_user(email=email, password=password)

        login(request, user)
        return JsonResponse({'message': 'User created successfully'})
