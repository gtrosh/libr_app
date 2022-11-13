from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import AuthorForm, BookForm, CollectionForm
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
            return redirect('/add_book/')
    
    form = AuthorForm()
    return render(request, 'add_author.html', {'form': form})


def get_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'The book successfully added to library')
            return redirect('/')
    form = BookForm()
    return render(request, 'add_book.html', {'form': form})


def add_to_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            book_title = data['books'][0]
            user_collection = Collection.objects.filter(owner=request.user)
            
            if not user_collection:
                
                collection = form.save(commit=False)
                collection.owner = request.user
                collection.save()
                new_book = Book.objects.filter(title=book_title)                
                collection.books.set([new_book[0]])
                messages.add_message(request, messages.SUCCESS, 'The book successfully added to collection')
                return redirect('/')
            
            else:
                collected_books = user_collection.iterator()
                
                for el in collected_books:
                    books_titles = el.books.values('title')
                    titles = []
                    for item in books_titles:
                        titles.append(item['title'])

                    if str(book_title) in titles:
                        messages.add_message(request, messages.INFO, 'This book is already in your collection')
                        return redirect('/')
                    else:
                        books = el.books.all()
                        new_book = Book.objects.filter(title=book_title)

                        book_list = list(books)
                        book_list.append(new_book[0])
                        user_collection[0].books.set(book_list)
                        messages.add_message(request, messages.SUCCESS, 'The book successfully added to collection')
                        return redirect('/')         
    form = CollectionForm()
    return render(request, 'add_collection.html', {'form': form})
