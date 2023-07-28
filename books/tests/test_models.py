from django.test import TestCase
from books.models import Author, Book


class AuthorModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = Author.objects.create(
            first_name="Иван", middle_name="Сидорович", last_name="Петров"
        )

    def test_first_name_label(self):
        author = AuthorModelTest.author
        verbose = author._meta.get_field("first_name").verbose_name
        self.assertEqual(verbose, "First name")

    def test_middle_name_label(self):
        author = AuthorModelTest.author
        verbose = author._meta.get_field("middle_name").verbose_name
        self.assertEqual(verbose, "Middle name")

    def test_last_name_label(self):
        author = AuthorModelTest.author
        verbose = author._meta.get_field("last_name").verbose_name
        self.assertEqual(verbose, "Last name")

    def test_object_name_is_first_and_last_name(self):
        author = AuthorModelTest.author
        expected_object_name = author.first_name + " " + author.last_name
        self.assertEqual(expected_object_name, "Иван Петров")


class BookModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author1 = Author.objects.create(
            first_name="Иван", middle_name="Сидорович", last_name="Петров"
        )
        cls.author2 = Author.objects.create(
            first_name="Сидор", middle_name="Петрович", last_name="Иванов"
        )
        cls.book = Book.objects.create(title="Тестовая книга")
        cls.book.authors.set([cls.author1, cls.author2])

    def test_title_label(self):
        book = BookModelTest.book
        verbose = book._meta.get_field("title").verbose_name
        self.assertEqual(verbose, "Title")

    def test_authors_label(self):
        book = BookModelTest.book
        verbose = book._meta.get_field("authors").verbose_name
        self.assertEqual(verbose, "Author")

    def test_object_name_is_title(self):
        book = BookModelTest.book
        expected_object_name = book.title
        self.assertEqual(expected_object_name, "Тестовая книга")

    def test_get_authors(self):
        book = BookModelTest.book
        expected_authors = ", ".join(
            [a.last_name for a in book.authors.all().order_by("last_name")]
        )
        self.assertEqual(expected_authors, "Иванов, Петров")
