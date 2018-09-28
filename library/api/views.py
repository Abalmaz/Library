from rest_framework import mixins, generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import BookSerializer
from mylib.models import Book

#
# class BookList(mixins.ListModelMixin,
#                generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#
# class BookDetail(mixins.RetrieveModelMixin,
#                  generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('title', 'authors', 'year', 'publishing')
    ordering_fields = ('title', 'year', 'authors')
