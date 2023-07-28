from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Author, Book, Collection, Note


class AuthorForm(forms.Form):
    last_name = forms.CharField(label="Author's last name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Author's first name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(label="Author's middle name (optional)", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


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
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['book', 'heading', 'text']

        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'heading': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }