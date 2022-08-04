from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse, resolve

from mylib.forms import BookForm
from mylib.models import Book, User, Author, Genre
from mylib.views import BookCreateView


class BookCreateTestCase(TestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'genre.json',
                     'PublishingHouse.json',
                     'user.json',
                     'user_publisher.json',
                     'author.json',
                     'book.json',
                     'm2m.json')
        self.user = User.objects.get(username="test_publisher")
        self.url = reverse('book_add')


class BookCreateTest(BookCreateTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_book_create_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_book_create_view_function(self):
        view = resolve('/profile/books/')
        self.assertEquals(view.func.view_class, BookCreateView)

    def test_book_create_form_contains(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, BookForm)

    def test_book_create_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, '<select', 2)
        self.assertContains(self.response, 'type="number"', 2)
        self.assertContains(self.response, '<textarea', 1)
        self.assertContains(self.response, 'type="file"', 1)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_book_create_valid_post_data(self):
        self.assertFalse(Book.objects.filter(title='Test book').exists())
        authors = [Author.objects.get(pk=1).pk]
        genres = [Genre.objects.get(pk=1).pk]
        data = {
            'title': 'Test book',
            'authors': authors,
            'genre': genres,
            'year': '2018',
            'number_page': '1',
            'description': 'test book',
            'publishing': self.user.publisher_profile.publishing_house
        }
        self.client.post(self.url, data)
        self.assertTrue(Book.objects.filter(title='Test book').exists())

    # def test_book_create_invalid_post_data(self):
    #     self.client.post(self.url, {})
    #     self.assertEquals(self.response.status_code, 200)
    #     form = self.response.context.get('form')
    #     self.assertTrue(form.errors)


class ReaderBookCreateTest(BookCreateTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.get(username="test_reader")
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_book_create_status_code(self):
        self.assertEquals(self.response.status_code, 403)


class LoginRequiredBookCreateTests(BookCreateTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.client.get(self.url),
                             '{login_url}?next={url}'.format(
                                 login_url=login_url,
                                 url=self.url))
