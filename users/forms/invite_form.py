from django import forms

from organizations.models import Organization


class InviteForm(forms.Form):
    email = forms.EmailField()
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.none(),
        empty_label="Select organization",
        required=True,
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            org_ids = user.user_organizations.values_list("organization_id", flat=True)
            self.fields["organization"].queryset = Organization.objects.filter(pk__in=org_ids)
