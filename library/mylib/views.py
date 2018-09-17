from django.db.models import Min
from .filter import BookFilter
from django.views.generic import DetailView, ListView

from .models import Book, Author


class AuthorInfoView(DetailView):
    context_object_name = 'author'
    queryset = Author.objects.all()


class BookInfoView(DetailView):
    context_object_name = 'book'
    queryset = Book.objects.all()


class BookListView(ListView):
    context_object_name = 'books'
    model = Book
    paginate_by = 5

    def get_ordering(self):
        return self.request.GET.get('order_by', 'pk')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['order_by'] = self.get_ordering()
        filter = BookFilter()
        context['filter'] = filter

        return context

    def get_queryset(self):
        order = self.get_ordering()

        if order == 'authors':
            queryset = Book.objects.annotate(x=Min('bookauthor__order')).order_by('x', 'authors__second_name')
        else:
            queryset = Book.objects.order_by(order)

        return BookFilter(self.request.GET, queryset=queryset).qs
        # return queryset
