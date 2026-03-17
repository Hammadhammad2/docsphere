from django import forms

from organizations.models import Organization


class CreateOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Organization name"}),
            "description": forms.Textarea(attrs={"placeholder": "Optional description", "rows": 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and Organization.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This organization name is already in use.")
        return name
