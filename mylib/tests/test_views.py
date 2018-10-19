from django.test import TestCase
from django.urls import reverse, resolve

from mylib.views import BookListView


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
        url = reverse('book_info')
        self.response = self.client.get(url)

    def test_book_detail_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_book_detail_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'mylib/book_detail.html')


class BookCreateTest(TestCase):
    pass


class BookDeleteTest(TestCase):
    pass


class AuthorDetailTest(TestCase):
    pass


class InvitationTest(TestCase):
    pass






