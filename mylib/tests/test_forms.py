from django.test import TestCase

from mylib.forms import SignUpForm


class SignUpFormTest(TestCase):
    class SignUpFormTest(TestCase):
        def test_form_has_fields(self):
            form = SignUpForm()
            expected = ['username', 'email', 'password1', 'password2',
                        'first_name', 'last_name', 'middle_name',
                        'birth_date', 'is_subscription']
            actual = list(form.fields)
            self.assertSequenceEqual(expected, actual)
