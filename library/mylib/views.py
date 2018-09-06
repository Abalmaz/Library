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
    paginate_by = 10

    def get_queryset(self):
        # order = 'title'
        order = self.request.GET.get('order_by', 'pk')
        new_context = Book.objects.all().order_by(order)
        return new_context
