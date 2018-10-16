from django.test import TestCase
from django.urls import reverse, resolve

from mylib.views import BookListView


class BookListTest(TestCase):
    def test_book_list_view_status_code(self):
        url = reverse('book_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_book_list_url_resolves_view(self):
        view = resolve('/')
        self.assertEquals(view.func, BookListView)


class BookDetailTest(TestCase):
    pass


class AuthorDetailTest(TestCase):
    pass


class BookCreateTest(TestCase):
    pass


class BookDeleteTest(TestCase):
    pass


class SignUpTest(TestCase):
    pass


class UserUpdateTest(TestCase):
    pass


class InvitationTest(TestCase):
    pass

