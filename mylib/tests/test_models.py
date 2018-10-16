from django.core.management import call_command
from django.test import TestCase
from mylib.models import Author, Book


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

    def test_full_name(self):
        expected_object_name = '{} {} {}' .format(self.author.second_name,
                                                  self.author.first_name,
                                                  self.author.middle_name)
        self.assertEquals(expected_object_name, self.author.full_name)

    def test_short_name(self):
        if self.author.pseudonym:
            expected_object_name = '{}'.format(self.author.pseudonym)
        elif self.middle_name:
            expected_object_name = '{} {}. {}.'.format(
                self.second_name,
                self.first_name[0].capitalize(),
                self.middle_name[0].capitalize()
            )
        else:
            expected_object_name = '{} {}.'.format(
                self.second_name,
                self.first_name[0].capitalize()
            )

        self.assertEquals(expected_object_name, self.author.short_name)


class BookModelTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'country.json',
                     'PublishingHouse.json', 'genre.json', 'author.json',
                     'book.json', 'm2m.json', verbosity=0)
        self.book = Book.objects.get(id=1)

    def test_title_max_length(self):
        max_length = self.book._meta.get_field('title').max_length
        self.assertEquals(max_length, 80)

    def test_object_name_is_title(self):
        expected_object_name = '{}'.format(self.book.title)
        self.assertEquals(expected_object_name, str(self.book))

    def test_get_absolute_url(self):
        self.assertEquals(self.book.get_absolute_url(), '/books/1/')
