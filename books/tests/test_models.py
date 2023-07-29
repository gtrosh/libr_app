from django.test import TestCase
from books.models import Author, Book, Note, Collection
from django.contrib.auth.models import User


class AuthorModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = Author.objects.create(
            first_name="Иван", middle_name="Сидорович", last_name="Петров"
        )

    def test_verbose_name(self):
        author = AuthorModelTest.author
        field_verboses = {
            "first_name": "First name",
            "middle_name": "Middle name",
            "last_name": "Last name",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    author._meta.get_field(field).verbose_name, expected_value
                )

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

    def test_verbose_name(self):
        book = BookModelTest.book
        field_verboses = {"title": "Title", "authors": "Author"}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    book._meta.get_field(field).verbose_name, expected_value
                )

    def test_object_name_is_title(self):
        book = BookModelTest.book
        expected_object_name = book.title
        self.assertEqual(expected_object_name, "Тестовая книга")

    def test_get_authors(self):
        book = BookModelTest.book
        expected_authors = book.get_authors()
        self.assertEqual(expected_authors, "Иванов, Петров")


class NoteModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.author = Author.objects.create(
            first_name="Иван", middle_name="Сидорович", last_name="Петров"
        )
        cls.book = Book.objects.create(title="Тестовая книга")
        cls.book.authors.set([cls.author])
        cls.note = Note.objects.create(
            user=cls.user,
            book=cls.book,
            heading="Заголовок заметки",
            text="Текст заметки",
        )

    def test_verbose_name(self):
        note = NoteModelTest.note
        field_verboses = {"heading": "Heading", "text": "Text", "added": "Date added"}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    note._meta.get_field(field).verbose_name, expected_value
                )

    def test_object_name_is_heading(self):
        note = NoteModelTest.note
        expected_object_name = note.heading
        self.assertEqual(expected_object_name, "Заголовок заметки")


class CollectionModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = Author.objects.create(
            first_name="Иван", middle_name="Сидорович", last_name="Петров"
        )
        cls.book1 = Book.objects.create(title="Тестовая книга 1")
        cls.book1.authors.set([cls.author])
        cls.book2 = Book.objects.create(title="Тестовая книга 2")
        cls.book2.authors.set([cls.author])
        cls.owner = User.objects.create_user(username="auth")
        cls.collection = Collection.objects.create(owner=cls.owner)
        cls.collection.books.set([cls.book1, cls.book2])

    def test_get_books(self):
        collection = CollectionModelTest.collection
        expected_books = collection.get_books()
        self.assertEqual(expected_books, "Тестовая книга 1, Тестовая книга 2")

    def test_object_name_is_owners_collection(self):
        collection = CollectionModelTest.collection
        expected_object_name = f"{collection.owner}'s collection"
        self.assertEqual(expected_object_name, "auth's collection")
