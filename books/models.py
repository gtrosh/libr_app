from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=20, verbose_name="First name")
    middle_name = models.CharField(
        max_length=20, blank=True, verbose_name="Middle name"
    )
    last_name = models.CharField(max_length=20, verbose_name="Last name")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["last_name"]
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    title = models.CharField(max_length=50, verbose_name="Title")
    authors = models.ManyToManyField(Author, verbose_name="Author")

    def get_authors(self):
        return ", ".join(
            [a.last_name for a in self.authors.all().order_by("last_name")]
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]
        verbose_name = "Book"
        verbose_name_plural = "Books"


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Book")
    heading = models.CharField(max_length=50, verbose_name="Heading")
    text = models.TextField(verbose_name="Text")
    added = models.DateTimeField(auto_now_add=True, verbose_name="Date added")

    def __str__(self):
        return f"{self.heading}"

    class Meta:
        ordering = ["-added", "book"]
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"


class Collection(models.Model):
    books = models.ManyToManyField(Book)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="collections", null=True
    )

    def get_books(self):
        return ", ".join([b.title for b in self.books.all()])

    def __str__(self):
        return f"{self.owner}'s collection"

    class Meta:
        ordering = ["owner"]
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"
