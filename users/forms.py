from django import forms
from django.contrib.auth import authenticate

from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, strip=False)

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data["email"]
        password = cleaned_data["password"]

        self.user = authenticate(self.request, username=email, password=password)
        if self.user is None:
            raise forms.ValidationError("Invalid email or password.")

        return cleaned_data


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
