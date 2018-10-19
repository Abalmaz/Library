from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse, resolve

from mylib.models import Book, User
from mylib.views import BookDeleteView


class BookDeleteTestCase(TestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'genre.json',
                     'PublishingHouse.json',
                     'author.json',
                     'user.json',
                     'user_publisher.json',
                     'book.json',
                     'm2m.json')
        self.user = User.objects.get(username="test_publisher")
        self.book = self.user.publisher_profile.publishing_house.book_set.all()[
                    0]
        self.url = reverse('book_delete', kwargs={'pk': self.book.pk})


class BookDeleteTest(BookDeleteTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_book_delete_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_book_delete_view_function(self):
        view = resolve('/profile/books/{}/delete/'.format(self.book.pk))
        self.assertEquals(view.func.view_class, BookDeleteView)

    def test_book_delete_view_inputs(self):
        self.assertContains(self.response, 'Are you sure you want to delete')

    def test_book_delete_check_result(self):
        book_id = self.book.id
        post = self.client.post(self.url)
        self.assertRedirects(post, reverse('profile'))
        self.assertFalse(Book.objects.filter(id=book_id).exists())

    def test_book_delete_not_found_status_code(self):
        url = reverse('book_delete', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


class LoginRequiredDeleteBookTest(BookDeleteTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response,
                             '{login_url}?next={url}'.format(
                                 login_url=login_url,
                                 url=self.url)
                             )


class NotOwnerBookDeleteTest(BookDeleteTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.get(username="test_publisher2")
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_book_delete_status_code(self):
        self.assertEquals(self.response.status_code, 403)

