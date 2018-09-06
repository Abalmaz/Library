from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Book, Author

# Create your views here.


class AuthorInfoView(DetailView):
    context_object_name = 'author'
    queryset = Author.objects.all()


class BookInfoView(DetailView):
    context_object_name = 'book'
    queryset = Book.objects.all()


class BookListView(ListView):
    model = Book
