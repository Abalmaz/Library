from django.urls import path
from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='index'),
    path('books/<int:pk>/', views.BookInfoView.as_view(), name='books_info'),
    path('authors/<int:pk>/', views.AuthorInfoView.as_view(), name='authors_info'),
]