import django_filters
# from django import forms
from .models import Book, Author, PublishingHouse


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(lookup_expr='year')
    # author = django_filters.ModelMultipleChoiceFilter(queryset=Author.objects.all(),
    #                                                   widget=forms.CheckboxSelectMultiple)
    # publisher = django_filters.ModelMultipleChoiceFilter(queryset=PublishingHouse.objects.all(),
    #                                                      widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Book
        fields = ['title', 'year', 'authors', 'publishing']