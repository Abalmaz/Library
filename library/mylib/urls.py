from django.urls import path
from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookInfoView.as_view(), name='book_info'),
    path('authors/<int:pk>/', views.AuthorInfoView.as_view(),
         name='author_info'),
]
