from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import reverse, resolve
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from mylib.models import User


class PasswordResetTest(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/password_reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)

    def test_pass_reset_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'registration/pass_reset.html')


class SuccessfulPasswordResetTest(TestCase):
    def setUp(self):
        email = 'test@mail.com'
        User.objects.create_user(username='test_pass_reset',
                                 email=email,
                                 password='Abcd1234')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordReset(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'invalidmail@mail.com'})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_dont_send_password_reset_email(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetMailTest(TestCase):
    def setUp(self):
        email = 'test@mail.com'
        User.objects.create_user(username='test_pass_reset',
                                 email=email,
                                 password='Abcd1234')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})
        self.out_email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[Library] Please reset your password',
                         self.out_email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.out_email.body)
        self.assertIn('test@mail.com', self.out_email.body)

    def test_email_to(self):
        self.assertEqual(['test@mail.com',], self.out_email.to)


class PasswordResetDone(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/password_reset/done/')
        self.assertEquals(view.func.view_class,
                          auth_views.PasswordResetDoneView)

    def test_signup_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,
                                'registration/pass_reset_done.html')


class PasswordResetConfirmTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_pass_reset',
                                        email='test@mail.com',
                                        password='Abcd1234')

        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid,
                                                        'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/password_reset/{}/{}/'.format(
            self.uid, self.token
        ))
        self.assertEquals(view.func.view_class,
                          auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)

    def test_signup_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,
                                'registration/pass_reset_confirm.html')


class InvalidPasswordResetConfirmTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_pass_reset',
                                        email='test@mail.com',
                                        password='Abcd1234')

        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        user.set_password('InvalidPass123')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': uid,
                                                        'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{}"'.format(
            password_reset_url))


class PasswordResetCompleteTest(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/password_reset/complete/')
        self.assertEquals(view.func.view_class,
                          auth_views.PasswordResetCompleteView)

    def test_pass_reset_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response,
                                'registration/pass_reset_complete.html')