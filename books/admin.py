from django.contrib import admin
from .models import Author, Book, Note, Collection


class BookAdmin(admin.ModelAdmin):
    fields = ['authors', 'title']
    list_display = ('get_authors', 'title')
    search_fields = ['authors__last_name', 'title']


class CollectionAdmin(admin.ModelAdmin):
    fields = ['owner', 'books']
    list_display = ('owner', 'get_books')



admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Note)
admin.site.register(Collection, CollectionAdmin)
