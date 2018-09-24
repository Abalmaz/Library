from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import login

from .mixins import PublisherRequiredMixin, OwnerRequiredMixin
from .filters import BookFilter
from .forms import SignUpForm
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import Book, Author, User, Invitation, PublishingHouse


class AuthorDetailView(DetailView):
    context_object_name = 'author'
    queryset = Author.objects.all()


class BookDetailView(DetailView):
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


class BookCreateView(PublisherRequiredMixin, CreateView):
    login_url = 'login'
    model = Book
    template_name = 'mylib/add_book.html'
    fields = ('title', 'authors', 'genre', 'year', 'number_page', 'description', 'cover')
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.publishing = PublishingHouse.objects.get(pk=self.request.user.publisher_profile.pk)
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
        login(self.request, user)
        return redirect('book_list')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = User
    fields = ('first_name', 'middle_name', 'last_name', 'birth_date', 'email')
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
    if not invite.is_invitation():
        return render(request, 'registration/invitation_error.html')
    user = invite.user

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = SetPasswordForm(user)

    return render(request, 'registration/invitation.html', {'form': form})

