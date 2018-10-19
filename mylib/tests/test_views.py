from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse, resolve

from mylib.models import Book, Author
from mylib.views import BookListView, BookDetailView, AuthorDetailView


class BookListTest(TestCase):
    def setUp(self):
        url = reverse('book_list')
        self.response = self.client.get(url)

    def test_book_list_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_book_list_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'mylib/book_list.html')

    def test_home_url_resolves_book_list_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BookListView)


class BookDetailTest(TestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'genre.json',
                     'PublishingHouse.json',
                     'author.json',
                     'book.json',
                     'm2m.json')
        self.book = Book.objects.get(id=1)
        url = reverse('book_info', kwargs={'pk': 1})
        self.response = self.client.get(url)

    def test_book_detail_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_book_detail_view_function(self):
        view = resolve('/books/1/')
        self.assertEquals(view.func.view_class, BookDetailView)

    def test_book_detail_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'mylib/book_detail.html')

    def test_book_detail_view_not_found_status_code(self):
        url = reverse('book_info', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


class AuthorDetailTest(TestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'genre.json',
                     'PublishingHouse.json',
                     'author.json',
                     'book.json',
                     'm2m.json')
        self.author = Author.objects.get(id=1)
        url = reverse('author_info', kwargs={'pk': 1})
        self.response = self.client.get(url)

    def test_author_detail_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_author_detail_view_function(self):
        view = resolve('/authors/1/')
        self.assertEquals(view.func.view_class, AuthorDetailView)

    def test_author_detail_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'mylib/author_detail.html')

    def test_author_detail_view_not_found_status_code(self):
        url = reverse('author_info', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


class InvitationTest(TestCase):
    pass






