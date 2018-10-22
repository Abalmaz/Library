from django.test import TestCase

from mylib.forms import SignUpForm


class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'password1', 'password2',
                    'first_name', 'last_name', 'email',
                    'birth_date', 'is_subscription', 'middle_name']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

