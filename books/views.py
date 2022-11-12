from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import AuthorForm, BookForm
from .models import Author, Book, Note, Collection 


def home(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 10, orphans=3, allow_empty_first_page=True)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    return render(request, 'home.html', {'books': books})


def search_books(request):
    if request.method == 'POST':
        book_searched = request.POST.get('book_searched', False)
        result = Book.objects.filter(Q(authors__last_name__contains=book_searched) | Q(title__contains=book_searched))
        return render(request, 'search_books.html', {'book_searched': book_searched, 'result': result})
    else:
        return render(request, 'search_books.html', {})


def get_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            last_name = data['last_name']
            first_name = data['first_name']
            middle_name = data['middle_name']
            author, _ = Author.objects.get_or_create(last_name=last_name, first_name=first_name, middle_name=middle_name)
            messages.add_message(request, messages.SUCCESS, 'The author added successfully')
            return redirect('/')
    
    form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})


def get_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'The book added successfully')
            return redirect('/')
    form = BookForm()
    return render(request, 'add_book.html', {'form': form})