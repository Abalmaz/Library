from rest_framework import serializers
from library.mylib.models import User, Book


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_reader', 'is_publisher')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('url', 'title', 'year', 'author', 'number_page', 'publishing',
                  'genre', 'description', 'cover', 'ratings')