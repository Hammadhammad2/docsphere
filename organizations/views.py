from django.http import HttpResponse

from organizations.models import Organization


def organization_list(request):
    organizations = Organization.objects.values("id", "name", "description", "created_at")
    print(list(organizations))
    return HttpResponse(list(organizations))


def organization_create(request):
    if request.method == "POST":
        organization = Organization.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            created_by=request.user
        )
        return HttpResponse(f"Organization {organization.id} created successfully")
    return HttpResponse("Organization creation failed")


def organization_detail(request, id):
    organization = Organization.objects.get(id=id)
    return HttpResponse(organization)


def organization_update(request, id):
    organization = Organization.objects.get(id=id)
    organization.name = request.POST.get("name")
    organization.description = request.POST.get("description")
    organization.save()
    return HttpResponse(organization)