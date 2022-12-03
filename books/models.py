from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ["last_name"]
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Book(models.Model):
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(Author)

    def get_authors(self):
        return ', '.join([a.last_name for a in self.authors.all()])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    heading = models.CharField(max_length=50)
    text = models.TextField()
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.added} - {self.heading}'

    class Meta:
        ordering = ["-added", "book"]
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"


class Collection(models.Model):
    books = models.ManyToManyField(Book)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections', null=True)

    def get_books(self):
        return ', '.join([b.title for b in self.books.all()])

    def __str__(self):
        return f"{self.owner}'s collection"

    class Meta:
        ordering = ["owner"]
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
