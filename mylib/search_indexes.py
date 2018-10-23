from haystack import indexes
from mylib.models import Author, Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,
                             template_name="search/book_text.txt"
                             )

    def get_model(self):
        return Book


class AuthorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,
                             template_name="search/author_text.txt")

    def get_model(self):
        return Author
