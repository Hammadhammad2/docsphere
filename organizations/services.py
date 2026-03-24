from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse


def send_organization_invite_email(invite, request):
    accept_url = request.build_absolute_uri(reverse("organizations:accept_invite", kwargs={"token": invite.token}))
    context = {
        "invite": invite,
        "organization": invite.organization,
        "accept_url": accept_url,
        "invited_by": invite.invited_by,
    }

    message = EmailMultiAlternatives(
        subject=render_to_string("organizations/email/invite_user_subject.txt", context).strip(),
        body=render_to_string("organizations/email/invite_user.txt", context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[invite.email],
    )

    message.attach_alternative(
        render_to_string("organizations/email/invite_user.html", context),
        "text/html",
    )

    message.send(fail_silently=False)
