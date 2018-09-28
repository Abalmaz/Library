from rest_framework import serializers
from star_ratings.models import Rating
from mylib.models import User, Book, PublishingHouse, Author, Genre, BookAuthor


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_reader', 'is_publisher')


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', )


class PublishingHouseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PublishingHouse
        fields = ('name', )


class BookAuthorSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.short_name')

    class Meta:
        model = BookAuthor
        fields = ('author', )


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = BookAuthorSerializer(source='bookauthor_set', many=True)
    publishing = PublishingHouseSerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    ratings = RatingSerializer()
    # ratings = serializers.SlugRelatedField(queryset=Rating.objects.all(),
    #                                        slug_field='average')

    class Meta:
        model = Book
        fields = ('url', 'title', 'year', 'number_page',
                  'authors',
                  'publishing',
                  'genre',
                  'description',
                  'cover',
                  'ratings')