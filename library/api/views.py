from django.shortcuts import render
from rest_framework import mixins, generics


# Create your views here.
from library.api.serializers import BookSerializer
from library.mylib.models import Book


class BookList(mixins.ListModelMixin,
               generics.GenericAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
