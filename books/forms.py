from django import forms
from django.forms import ModelForm
from .models import Author, Book, Collection, Note


class AuthorForm(forms.Form):
    last_name = forms.CharField(label="Author's last name", max_length=100)
    first_name = forms.CharField(label="Author's first name", max_length=100)
    middle_name = forms.CharField(label="Author's middle name (optional)", max_length=100, required=False)


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['authors', 'title']


class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = ['books']
