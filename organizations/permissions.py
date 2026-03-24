from organizations.choices import Role
from organizations.models import UserOrganization


def user_can_manage_org(user, organization):
    return UserOrganization.objects.filter(
        organization=organization,
        user=user,
        role__in=(Role.OWNER, Role.ADMIN),
    ).exists()
