import django_filters
from django import forms
from .models import Book, PublishingHouse


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    publishing = django_filters.ModelMultipleChoiceFilter \
        (queryset=PublishingHouse.objects.all(),
         widget=forms.CheckboxSelectMultiple)
    o = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('year', 'year'),
            ('authors', 'authors')
        ),
    )

    class Meta:
        model = Book
        fields = ['title', 'year', 'authors', 'publishing']
