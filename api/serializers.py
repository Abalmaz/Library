from rest_framework import serializers
from mylib.models import User, Book, PublishingHouse, Country, \
                         Author, Genre, BookAuthor


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_reader', 'is_publisher')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PublishingHouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublishingHouse
        fields = '__all__'


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'url', 'short_name', )


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True)
    publishing = PublishingHouseSerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating_avg = serializers.FloatField()

    class Meta:
        model = Book
        fields = ('url', 'title', 'year', 'number_page',
                  'authors',
                  'publishing',
                  'genre',
                  'description',
                  'cover',
                  'rating_avg',
                  )


class AuthorDetailSerializer(serializers.HyperlinkedModelSerializer):
    country = CountrySerializer()
    genre = GenreSerializer(many=True)
    count_books_after_1910 = serializers.IntegerField()
    avg_page = serializers.IntegerField()
    min_page_before_1910 = serializers.IntegerField()
    avg_rating = serializers.FloatField()
    max_rating = serializers.FloatField()

    class Meta:
        model = Author
        fields = ('__all__')

