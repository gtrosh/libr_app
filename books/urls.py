from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search_books/', views.search_books, name='search-books'),
    path('add_author/', views.get_author, name='add-author'),
    path('add_book/', views.get_book, name='add-book'),
    path('add_collection/', views.add_to_collection, name='add-collection'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('add_note/', views.add_note, name='add-note'),
    path('collection/<str:username>/', views.get_collection, name='user-collection'),
    path('delete/<int:note_id>/', views.delete_note, name='note_delete'),
    path('collection/notes/<int:note_id>/', views.note_view, name='note'),
    path('collection/books/<int:book_id>/', views.book_view, name='book'),
    path('collection/notes/<str:username>/<int:note_id>/edit/', views.edit_note, name='note_edit'),
]

