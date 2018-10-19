from django.core.management import call_command
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, resolve

from mylib.models import User, PublishingHouse, Publisher
from mylib.views import UserUpdateView


class UserProfileTestBase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'Abcd1234'
        self.user = User.objects.create_user(username=self.username,
                                             email='test@gmail.com',
                                             password=self.password)
        self.url = reverse('profile')
        self.client.login(username=self.username, password=self.password)


class UserProfileTest(UserProfileTestBase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve('/profile/')
        self.assertEquals(view.func.view_class, UserUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 7)
        self.assertContains(self.response, 'type="text"', 4)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="checkbox"', 1)
        self.assertNotContains(self.response, '<p>Books:')


class LoginRequiredUserProfileTest(TestCase):
    def test_redirection(self):
        url = reverse('profile')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, '{}?next={}'.format(login_url, url))


class SuccessfulUserUpdateTest(UserProfileTestBase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'middle_name': 'FooBar',
            'is_subscription': True,
        })

    def test_redirection(self):
        self.assertRedirects(self.response, self.url)

    def test_data_changed(self):
        self.user.refresh_from_db()
        self.assertEquals('Foo', self.user.first_name)
        self.assertEquals('Bar', self.user.last_name)
        self.assertEquals('FooBar', self.user.middle_name)
        self.assertTrue(self.user.is_subscription)


class InvalidUserUpdateTest(UserProfileTestBase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {
            'first_name': 'Foo'*100
        })

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_user_profile(self):
        self.user.refresh_from_db()
        self.assertEquals('', self.user.first_name)


class UserProfilePublisherTestBase(TestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'PublishingHouse.json',
                     'genre.json',
                     'author.json',
                     'book.json',
                     'm2m.json',
                     verbosity=0)
        self.username = 'test_pub'
        self.password = 'Abcd1234'
        self.user = User.objects.create_user(username=self.username,
                                             email='test@gmail.com',
                                             is_publisher=True,
                                             password=self.password)
        Publisher.objects.create(user=self.user,
                                 publishing_house=PublishingHouse.objects.last())
        self.url = reverse('profile')
        self.client.login(username=self.username, password=self.password)


class UserProfilePublisherTest(UserProfilePublisherTestBase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_contains_book_list(self):
        self.assertContains(self.response, '<ul', 2)
        self.assertContains(self.response, '<p>Books:', 1)
        self.assertContains(self.response, 'Add book</a>', 1)
