from django.urls import path
from django.contrib.auth import views as auth_views
from haystack.views import SearchView

from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_info'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(),
         name='author_info'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
            template_name='registration/pass_reset.html',
            email_template_name='registration/pass_reset_email.html',
            subject_template_name='registration/pass_reset_subject.txt'
            ),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/pass_reset_done.html'),
        name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/pass_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/pass_reset_complete.html'),
        name='password_reset_complete'),
    path('password/change_password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/pass_change.html'),
        name='password_change'),
    path('password/change_password/done/',
         auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/pass_change_done.html'),
        name='password_change_done'),
    path('invitation/<uuid:token>', views.invitation, name='invitation'),
    path('profile/', views.UserUpdateView.as_view(), name='profile'),
    path('profile/books/', views.BookCreateView.as_view(), name='book_add'),
    path('profile/books/<int:pk>/delete/', views.BookDeleteView.as_view(),
         name='book_delete'),
    path('search/', SearchView(), name='search'),
]
