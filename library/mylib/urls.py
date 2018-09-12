from django.urls import path
from django_filters.views import FilterView
from .filter import BookFilter
from . import views


urlpatterns = [
    path('', FilterView.as_view(filterset_class=BookFilter, template_name='mylib/book_list.html'), name='book_list'),
    path('books/<int:pk>/', views.BookInfoView.as_view(), name='book_info'),
    path('authors/<int:pk>/', views.AuthorInfoView.as_view(), name='author_info'),
]