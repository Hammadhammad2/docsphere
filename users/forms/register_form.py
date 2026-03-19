from django import forms

from users.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    def clean_email(self):
        email = super().clean_email()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
