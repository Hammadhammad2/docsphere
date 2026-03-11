from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class ApiView(View):
    """
    Base view for all API endpoints.
    Exempt from CSRF so external clients (Postman, frontends) can call freely.
    """
