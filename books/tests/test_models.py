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

    def test_heading_label(self):
        note = NoteModelTest.note
        verbose = note._meta.get_field("heading").verbose_name
        self.assertEqual(verbose, "Heading")

    def test_text_label(self):
        note = NoteModelTest.note
        verbose = note._meta.get_field("text").verbose_name
        self.assertEqual(verbose, "Text")

    def test_added_label(self):
        note = NoteModelTest.note
        verbose = note._meta.get_field("added").verbose_name
        self.assertEqual(verbose, "Date added")

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
