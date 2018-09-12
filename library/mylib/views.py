from django.shortcuts import render
from django.db.models import Min
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
    paginate_by = 5

    def get_ordering(self):
        return self.request.GET.get('order_by', 'pk')

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['order_by'] = self.get_ordering()
        return context

    def get_queryset(self):
        order = self.get_ordering()
        if order == 'authors__second_name':
            new_context = Book.objects.annotate(x=Min('bookauthor__order')).order_by('x', order)
        else:
            new_context = Book.objects.order_by(order)
        return new_context
