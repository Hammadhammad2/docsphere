import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from config.views import ApiView

from .models import Organization


class OrganizationListView(ApiView):
    def get(self, request):
        organizations = Organization.objects.all()
        return JsonResponse(list(organizations))


class OrganizationCreateView(ApiView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return JsonResponse(
                {"error": "Only super admins can create organizations"},
                status=403,
            )

        try:
            data = json.loads(request.body)

            name = data.get("name")
            description = data.get("description", "")

            if not name:
                return JsonResponse(
                    {"error": "Name is required"},
                    status=400,
                )

            organization = Organization.objects.create(
                name=name,
                description=description,
            )

            return JsonResponse(
                {
                    "message": "Organization created successfully",
                    "id": organization.id,
                    "name": organization.name,
                    "description": organization.description,
                },
                status=201,
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)


class OrganizationDetailView(ApiView):
    def get(self, request, id):
        organization = get_object_or_404(Organization, id=id)
        print(organization)
        return JsonResponse({
            "message": "Organization retrieved successfully",
            "id": organization.id,
            "name": organization.name,
            "description": organization.description,
        })


class OrganizationUpdateView(ApiView):
    def put(self, request, id):
        try:
            organization = Organization.objects.get(id=id)

            data = json.loads(request.body)

            organization.name = data.get("name")
            organization.description = data.get("description")

            organization.save()

            return JsonResponse({
                "message": "Organization updated successfully",
                "id": organization.id,
                "name": organization.name,
                "description": organization.description,
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)
