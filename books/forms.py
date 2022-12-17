from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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

        widgets = {
            'authors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = ['books']

        widgets = {
            'books': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ('book', 'heading', 'text')