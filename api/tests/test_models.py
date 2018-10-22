from django.core.management import call_command
from django.test import TestCase

from mylib.models import Book, Author


class TestBookModel(TestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'PublishingHouse.json',
                     'genre.json',
                     'author.json',
                     'book.json',
                     'm2m.json')
        self.book = Book.objects.get(id=1)

    def test_book_object_name(self):
        self.assertEqual(self.book.title, str(self.book))


class TestAuthorModel(TestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'PublishingHouse.json',
                     'genre.json',
                     'author.json',
                     'book.json',
                     'm2m.json')
        self.book = Author.objects.get(id=1)

    def test_author_object_name(self):
        self.assertEqual(self.author.second_name, str(self.author))
