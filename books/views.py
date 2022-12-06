from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import AuthorForm, BookForm, CollectionForm, CreationForm, NoteForm
from .models import Author, Book, Note, Collection 


def home(request):
    book_list = Book.objects.all()
    user_books = []
    if request.user.is_authenticated:
        collection = get_object_or_404(Collection, owner=request.user)
        user_books = collection.books.values_list('title', flat=True)        
    
    paginator = Paginator(book_list, 10, orphans=3, allow_empty_first_page=True)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    context = {
        'paginator': paginator,
        'page': page,
        'books': books,
        'user_books': user_books
    }
    return render(request, 'home.html', context)


def search_books(request):
    if request.method == 'POST':
        book_searched = request.POST.get('book_searched', False)
        result = Book.objects.filter(Q(authors__last_name__contains=book_searched) | Q(title__contains=book_searched))
        return render(request, 'search_books.html', {'book_searched': book_searched, 'result': result})
    else:
        return render(request, 'search_books.html', {})


@login_required
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


@login_required
def get_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'The book successfully added to library')
            return redirect('/')
    form = BookForm()
    return render(request, 'add_book.html', {'form': form})


@login_required
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


@login_required
def get_collection(request, username):
    user_collection = get_object_or_404(Collection, owner__username=username)
    collection_owner = user_collection.owner
    books = user_collection.books
    result = []
    for book in books.all():
        title = book.title
        authors = []
        author_queryset = book.authors.all().values_list('last_name', flat=True)
        for el in author_queryset:
            authors.append(el)
        author_list = ', '.join(authors)
        data = (author_list, title)
        str_data = ' - '.join(data)
        data_dict = {}
        data_dict[book.id] = str_data
        result.append(data_dict)
    return render(request, 'collection.html', {'collection': user_collection, 'owner': collection_owner, 'result': result, 'data_dict': data_dict})
    

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            book_note = data['book']
            
            user_collection = Collection.objects.filter(owner=request.user)
            collected_books = user_collection.iterator()

            for el in collected_books:
                books_titles = el.books.values('title')
                titles = []
                for item in books_titles:
                    titles.append(item['title'])

                if str(book_note) in titles:
                    note = form.save(commit=False)
                    note.user = request.user
                    note.heading = data['heading']
                    note.text = data['text']
                    note.save()

                    book_name = Book.objects.filter(title=book_note)
                    note.book = book_name[0]
                    messages.add_message(request, messages.SUCCESS, 'Note has been added')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.INFO, 'Please add the book to your collection first')
                    return redirect('/add_collection')
                      
    form = NoteForm()
    return render(request, 'add_note.html', {'form': form})


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('home')
    template_name = "signup.html"


@login_required
def book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    notes = Note.objects.filter(book=book, user=request.user)
    
    context = {'book': book, 'notes': notes}
    return render(request, 'book.html', context)


@login_required
def note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    context = {'note': note}
    return render(request, 'note.html', context)