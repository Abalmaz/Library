from rest_framework import serializers
from mylib.models import User, Book, PublishingHouse, Author, Genre, BookAuthor


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_reader', 'is_publisher')


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


class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('__all__')


class BookAuthorSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = BookAuthor
        fields = ('author', )


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = BookAuthorSerializer(source='bookauthor_set', many=True)
    publishing = PublishingHouseSerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating_avg = serializers.SerializerMethodField()

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

    def get_rating_avg(self, obj):
        if obj.ratings.exists():
            return obj.ratings.first().average
        else:
            return 0
