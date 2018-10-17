from django.test import TestCase
from django.urls import reverse


class BookListTest(TestCase):
    def test_book_list_view_status_code(self):
        response = self.client.get(reverse('book_list'))
        self.assertEquals(response.status_code, 200)

    def test_book_list_view_uses_correct_template(self):
        response = self.client.get(reverse('book_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mylib/book_list.html')


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

