from django import forms

from documents.models import Document


class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ("title", "body")


class DocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ("title", "body")
