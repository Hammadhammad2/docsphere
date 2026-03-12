import json
from http import HTTPStatus

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
                {'error': 'Only super admins can create organizations'},
                status=HTTPStatus.FORBIDDEN,
            )

        try:
            data = json.loads(request.body)

            name = data.get('name')
            description = data.get('description', '')

            if not name:
                return JsonResponse(
                    {'error': 'Name is required'},
                    status=HTTPStatus.BAD_REQUEST,
                )

            organization = Organization.objects.create(
                name=name,
                description=description,
            )

            return JsonResponse(
                {
                    'message': 'Organization created successfully',
                    'id': organization.id,
                    'name': organization.name,
                    'description': organization.description,
                },
                status=HTTPStatus.CREATED,
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON body'},
                status=HTTPStatus.BAD_REQUEST,
            )


class OrganizationDetailView(ApiView):
    def get(self, request, organization_id):
        organization = get_object_or_404(Organization, pk=organization_id)

        return JsonResponse(
            {
                'message': 'Organization retrieved successfully',
                'id': organization.id,
                'name': organization.name,
                'description': organization.description,
            }
        )


class OrganizationUpdateView(ApiView):
    def put(self, request, organization_id):
        try:
            organization = Organization.objects.get(pk=organization_id)

            data = json.loads(request.body)

            organization.name = data.get('name')
            organization.description = data.get('description')

            organization.save()

            return JsonResponse(
                {
                    'message': 'Organization updated successfully',
                    'id': organization.id,
                    'name': organization.name,
                    'description': organization.description,
                }
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Invalid JSON body'},
                status=HTTPStatus.BAD_REQUEST,
            )
