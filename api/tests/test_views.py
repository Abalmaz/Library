from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from mylib.models import Book, Author


class TestBookView(APITestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'PublishingHouse.json',
                     'genre.json',
                     'author.json',
                     'book.json',
                     'm2m.json')

    def test_book_list_status_code(self):
        response = self.client.get(reverse('book-list'), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, )

    def test_book_detail_status_code(self):
        response = self.client.get(reverse('book-detail',
                                           kwargs={'pk': 1}),
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, )

    def test_getting_books(self):
        response = self.client.get(reverse('book-list'), format="json")
        self.assertEqual(response.data["count"], 7)

    def test_book_detail_getting_book(self):
        book = Book.objects.get(id=1)
        response = self.client.get(reverse('book-detail',
                                           kwargs={'pk': 1}),
                                   format="json")
        self.assertEqual(response.data["title"], book.title)

    def test_book_detail_not_found(self):
        response = self.client.get(reverse('book-detail',
                                           kwargs={'pk': 99999}),
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, )


class TestAuthorView(APITestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'PublishingHouse.json',
                     'genre.json',
                     'author.json',
                     'book.json',
                     'm2m.json')

    def test_author_list_status_code(self):
        response = self.client.get(reverse('book-list'), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, )

    def test_getting_authors(self):
        response = self.client.get(reverse('author-list'), format="json")
        self.assertEqual(response.data["count"], 7)

    def test_author_detail_getting_book(self):
        author = Author.objects.get(id=1)
        response = self.client.get(reverse('author-detail',
                                           kwargs={'pk': 1}),
                                   format="json")
        self.assertEqual(response.data["second_name"], author.second_name)

    def test_author_detail_not_found(self):
        response = self.client.get(reverse('author-detail',
                                           kwargs={'pk': 99999}),
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, )
