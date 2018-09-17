import django_filters
from django import forms
from .models import Book, Author, PublishingHouse


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    # year = django_filters.NumberFilter()
    # authors = django_filters.ModelMultipleChoiceFilter(queryset=Author.objects.all(),
    #                                                   widget=forms.CheckboxSelectMultiple),
    publishing = django_filters.ModelMultipleChoiceFilter(queryset=PublishingHouse.objects.all(),
                                                          widget=forms.CheckboxSelectMultiple)

    o = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('year', 'year'),
            ('authors', 'authors')
        )
    )


    class Meta:
        model = Book
        fields = ['title', 'year', 'authors', 'publishing']


