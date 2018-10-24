from django.contrib.auth.forms import SetPasswordForm
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse, resolve

from mylib.forms import CommentForm
from mylib.models import Book, Author, User, Invitation, Comment
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


class BookDetailTestCase(TestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'genre.json',
                     'PublishingHouse.json',
                     'author.json',
                     'book.json',
                     'user.json',
                     'm2m.json')
        self.book = Book.objects.get(id=1)
        self.user = User.objects.get(username='test_reader')
        self.url = reverse('book_info', kwargs={'pk': 1})


class BookDetailTest(BookDetailTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

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

    def test_comments_form_contain(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CommentForm)

    def test_template_show_comment_form_for_auth_user(self):
        self.assertContains(self.response, 'class="comment-form"', 1)


class BookDetailNotAuthUserTest(BookDetailTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_template_doesnt_show_comment_form_for_not_auth_user(self):
        self.assertNotContains(self.response, 'class="comment-form"')


class CommentTest(TestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'genre.json',
                     'PublishingHouse.json',
                     'author.json',
                     'book.json',
                     'm2m.json',
                     'user.json')
        self.user = User.objects.get(username='test_reader')
        self.book = Book.objects.get(id=1)
        self.url = reverse('book_info', kwargs={'pk': 1})

    def test_comment_create_for_auth_user(self):
        self.client.force_login(self.user)
        data = {
            'text': 'test comment',
        }
        self.client.post(self.url, data)
        self.assertTrue(Comment.objects.filter(text='test comment').exists())


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
    def setUp(self):
        call_command('loaddata',
                     'user.json')
        self.user = User.objects.get(username="test_publisher")
        self.inv = Invitation.objects.get(user=self.user.pk)
        self.url = reverse('invitation', kwargs={'token': self.inv.auth_token})
        self.response = self.client.get(self.url)
        self.home_url = reverse('book_list')

    def test_invitation_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_invitation_form_contain(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, 'type="password"', 2)

    def test_signup_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,
                                'registration/invitation.html')
