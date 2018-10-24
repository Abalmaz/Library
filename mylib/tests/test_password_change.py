from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.test import TestCase
from django.urls import reverse, resolve

from mylib.models import User


class PasswordChangeViewTest(TestCase):
    def setUp(self):
        username = 'test'
        password = 'Abcd123'
        User.objects.create_user(username=username,
                                 email='test@mail.com',
                                 password=password)
        url = reverse('password_change')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve('/password/change_password/')
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)

    def test_signup_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,
                                'registration/pass_change.html')


class PasswordChangeTestBase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='test',
                                             email='test@mail.com',
                                             password='Abcd1234')
        self.url = reverse('password_change')
        self.client.login(username='test', password='Abcd1234')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTest(PasswordChangeTestBase):
    def setUp(self):
        super().setUp({
            'old_password': 'Abcd1234',
            'new_password1': '4321dcbA',
            'new_password2': '4321dcbA',
        })

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('4321dcbA'))

    def test_user_authentication(self):
        response = self.client.get(reverse('book_list'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTest(PasswordChangeTestBase):
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Abcd1234'))
