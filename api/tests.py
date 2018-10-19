from django.core.management import call_command
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from mylib.models import Book


class ApiBookListTest(APITestCase):
    def setUp(self):
        call_command('loaddata',
                     'country.json',
                     'genre.json',
                     'PublishingHouse.json',
                     'author.json',
                     'book.json',
                     'm2m.json')
        self.url = '/api/books/'
        self.response = self.client.get(self.url)

    def test_api_book_list_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_api_api_book_list_get_book(self):
        # books = Book.objects.all()
        self.assertContains(self.response, {
            "url": "http://127.0.0.1:8000/api/books/1/",
            "title": "To Kill a Mockingbird",
            "year": 1960,
            "number_page": 281})


class ApiBookDetailTest(APITestCase):
    pass


class ApiAuthorListTest(APITestCase):
    pass


class ApiAuthorDetailTest(APITestCase):
    pass