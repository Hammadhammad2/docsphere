from django.forms import EmailField, Form, ModelForm, Textarea, TextInput, ValidationError

from organizations.models import Organization, OrganizationInvite, UserOrganization


class CreateOrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "description"]
        widgets = {
            "name": TextInput(attrs={"placeholder": "Organization name"}),
            "description": Textarea(attrs={"placeholder": "Optional description", "rows": 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and Organization.objects.filter(name__iexact=name).exists():
            raise ValidationError("This organization name is already in use.")
        return name


class UpdateOrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "description"]
        widgets = {
            "name": TextInput(attrs={"placeholder": "Organization name"}),
            "description": Textarea(attrs={"placeholder": "Optional description", "rows": 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and Organization.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This organization name is already in use.")
        return name


class CreateOrganizationInviteForm(Form):
    email = EmailField(label="Email address")

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop("organization", None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]

        if OrganizationInvite.objects.filter(
            email=email,
            organization=self.organization,
        ).exists():
            raise ValidationError("This email is already invited to this organization.")

        if UserOrganization.objects.filter(
            user__email=email,
            organization=self.organization,
        ).exists():
            raise ValidationError("This user is already a member of this organization.")

        return email
