from datetime import datetime, timedelta
from django.core import mail

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from mylib.models import Author, Book, Country, Genre, PublishingHouse, \
                         User, Invitation


class AuthorModelTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'country.json',
                     'genre.json', 'author.json', verbosity=0)
        self.author = Author.objects.get(id=1)

    def test_first_name_max_length(self):
        max_length = self.author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 25)

    def test_second_name_max_length(self):
        max_length = self.author._meta.get_field('second_name').max_length
        self.assertEquals(max_length, 25)

    def test_middle_name_max_length(self):
        max_length = self.author._meta.get_field('middle_name').max_length
        self.assertEquals(max_length, 25)

    def test_object_name_is_second_name(self):
        expected_object_name = '{}'.format(self.author.second_name)
        self.assertEquals(expected_object_name, str(self.author))

    def test_full_name(self):
        expected_object_name = '{} {} {}' .format(self.author.second_name,
                                                  self.author.first_name,
                                                  self.author.middle_name)
        self.assertEquals(expected_object_name, self.author.full_name)

    def test_short_name_has_pseudonym(self):
        expected_object_name = '{}'.format(self.author.pseudonym)
        self.assertEquals(expected_object_name, self.author.short_name)

    def test_short_name_has_middle_name(self):
        author = Author.objects.get(id=4)
        expected_object_name = '{} {}. {}.'.format(
            author.second_name,
            author.first_name[0].capitalize(),
            author.middle_name[0].capitalize()
        )
        self.assertEquals(expected_object_name, author.short_name)

    def test_short_name_dont_has_middle_name(self):
        author = Author.objects.get(id=7)
        expected_object_name = '{} {}.'.format(
            author.second_name,
            author.first_name[0].capitalize()
        )
        self.assertEquals(expected_object_name, author.short_name)


class BookModelTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'country.json',
                     'PublishingHouse.json', 'genre.json', 'author.json',
                     'book.json', 'm2m.json', verbosity=0)
        self.book = Book.objects.get(id=1)

    def test_title_max_length(self):
        max_length = self.book._meta.get_field('title').max_length
        self.assertEquals(max_length, 80)

    def test_recent_year(self):
        futuredate = datetime.now() + timedelta(days=365)
        self.book.year = futuredate.year
        with self.assertRaises(ValidationError):
            self.book.save()
            self.book.full_clean()

    def test_before_1000_year(self):
        self.book.year = 900
        with self.assertRaises(ValidationError):
            self.book.save()
            self.book.full_clean()

    def test_negative_page(self):
        self.book.number_page = -100
        with self.assertRaises(ValidationError):
            self.book.save()
            self.book.full_clean()

    def test_zero_page(self):
        self.book.number_page = 0
        with self.assertRaises(ValidationError):
            self.book.save()
            self.book.full_clean()

    def test_object_name_is_title(self):
        expected_object_name = '{}'.format(self.book.title)
        self.assertEquals(expected_object_name, str(self.book))

    def test_get_absolute_url(self):
        self.assertEquals(self.book.get_absolute_url(), '/books/1/')


class CountryModelTest(TestCase):
    def setUp(self):
        call_command('loaddata', 'country.json', verbosity=0)
        self.country = Country.objects.get(id=1)

    def test_country_name_max_length(self):
        max_length = self.country._meta.get_field('name').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_country_name(self):
        expected_object_name = '{}'.format(self.country.name)
        self.assertEquals(expected_object_name, str(self.country))


class GenreModelTest(TestCase):
    def setUp(self):
        call_command('loaddata', 'genre.json', verbosity=0)
        self.genre = Genre.objects.get(id=1)

    def test_genre_name_max_length(self):
        max_length = self.genre._meta.get_field('name').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_genre_name(self):
        expected_object_name = '{}'.format(self.genre.name)
        self.assertEquals(expected_object_name, str(self.genre))


class PublishingHouseModelTest(TestCase):
    def setUp(self):
        call_command('loaddata', 'country.json',
                     'PublishingHouse.json', verbosity=0)
        self.publisher = PublishingHouse.objects.get(id=1)

    def test_publisher_name_max_length(self):
        max_length = self.publisher._meta.get_field('name').max_length
        self.assertEquals(max_length, 35)

    def test_object_name_is_publisher_name(self):
        expected_object_name = '{}'.format(self.publisher.name)
        self.assertEquals(expected_object_name, str(self.publisher))


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='Weter1234')

    def test_middle_name_max_length(self):
        max_length = self.user._meta.get_field('middle_name').max_length
        self.assertEquals(max_length, 25)

    def test_default_is_reader(self):
        self.assertTrue(self.user.is_reader)


class InvitationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='Weter1234',
                                             is_publisher=True,
                                             email='test@mail.com')
        self.inv = Invitation.objects.get(user=self.user)

    def test_create_inv_for_publisher_user(self):
        self.assertTrue(self.inv)

    def test_send_invitation(self):
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'You have been invited to signup to Library')
        self.assertIn('{}'.format(self.inv.auth_token), mail.outbox[0].body)

    def test_get_absolute_url(self):
        self.assertEquals(self.inv.get_absolute_url(), '/invitation/{}'.format(
            self.inv.auth_token))

    def test_is_valid_auth_token_today(self):
        day = timezone.now()
        self.inv.created_at = day
        self.assertTrue(self.inv.is_valid())

    def test_is_valid_auth_token_yesterday(self):
        day = timezone.now() + timedelta(hours=-25)
        self.inv.created_at = day
        self.assertFalse(self.inv.is_valid())


