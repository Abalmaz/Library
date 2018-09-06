from django.contrib import admin
from .models  import Book, Author, PublishingHouse, Genre, Country

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Genre)
admin.site.register(Country)
