from django.db import models

# Create your models here.


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    pass


class Genre(models.Model):
    pass


class PublishingHouse(Timestamp):
    pass


class Author(Timestamp):
    pass


class Book(Timestamp):
    title = models.CharField(unique=True, max_length=80)
    year = models.IntegerField(max_length=4)
    number_page = models.IntegerField()
    publishing = models.ForeignKey(PublishingHouse, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Author, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField()