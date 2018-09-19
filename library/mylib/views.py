from django.shortcuts import redirect
from django.contrib.auth import login
from .filters import BookFilter
from .forms import SignUpForm
from django.views.generic import DetailView, ListView, CreateView

from .models import Book, Author, User


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        filter = BookFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filter

        return context

    def get_queryset(self):
        return BookFilter(self.request.GET, queryset=Book.objects.all()).qs


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('book_list')