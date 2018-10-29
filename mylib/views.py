from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .mixins import PublisherRequiredMixin, OwnerRequiredMixin
from .filters import BookFilter
from .forms import SignUpForm, CommentForm, BookForm
from django.views.generic import DetailView, ListView, CreateView, \
    UpdateView, DeleteView

from .models import Book, Author, User, Invitation, Comment


class AuthorDetailView(DetailView):
    context_object_name = 'author'
    queryset = Author.objects.all()


@method_decorator(cache_page(60 * 5, key_prefix='book'), name='dispatch')
class BookDetailView(DetailView):
    context_object_name = 'book'
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = self.get_object().comments.all()
        ctx['form'] = CommentForm()

        return ctx

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        book = self.get_object()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.book = book
            parent = form['parent'].value()
            if parent:
                obj.parent = Comment.objects.get(pk=parent)
            obj.author = request.user
            obj.text = form.cleaned_data['text']
            obj.save()
            return redirect('book_info', pk=book.pk)


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


class BookCreateView(PublisherRequiredMixin, CreateView):
    login_url = 'login'
    success_url = reverse_lazy('profile')
    model = Book
    form_class = BookForm
    template_name = 'mylib/add_book.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.publishing = self.request.user.publisher_profile.publishing_house
        obj.save()
        return super().form_valid(form)


class BookDeleteView(PublisherRequiredMixin, OwnerRequiredMixin, DeleteView):
    login_url = 'login'
    model = Book
    success_url = reverse_lazy('profile')


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user,
              backend='django.contrib.auth.backends.ModelBackend')
        return redirect('book_list')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = User
    fields = ('first_name', 'middle_name',
              'last_name', 'birth_date',
              'email', 'is_subscription')
    template_name = 'mylib/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        email_field = form.fields.get('email')
        email_field.disabled = True
        return form


def invitation(request, token):
    invite = get_object_or_404(Invitation, auth_token=token)
    if not invite.is_valid():
        return render(request, 'registration/invitation_error.html')
    user = invite.user

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('book_list')
    else:
        form = SetPasswordForm(user)

    return render(request, 'registration/invitation.html', {'form': form})
