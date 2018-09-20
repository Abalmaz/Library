from django.contrib import admin
from .models import Book, Author, PublishingHouse, Genre, Country, BookAuthor, User, Publisher

# Register your models here.


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


class BookAdmin(admin.ModelAdmin):
    inlines = (BookAuthorInline,)


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(User)
admin.site.register(Publisher)
