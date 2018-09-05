from django.db import models

# Create your models here.


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(unique=True, max_length=20)


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=20)


class PublishingHouse(Timestamp):
    name = models.CharField(max_length=35)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Author(Timestamp):
    first_name = models.CharField(max_length=25)
    second_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25)
    pseudonym = models.CharField(max_length=25)
    birth_date = models.DateField()
    death_date = models.DateField()
    biography = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre, on_delete=models.CASCADE)
    photo = models.ImageField()


class Book(Timestamp):
    title = models.CharField(unique=True, max_length=80)
    year = models.IntegerField(max_length=4)
    number_page = models.IntegerField()
    publishing = models.ForeignKey(PublishingHouse, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    cover = models.ImageField()