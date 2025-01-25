from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.library_example.docs.api import BOOK_BASE_SERIALIZER_EXAMPLES
from apps.library_example.models import Book


class AuthorBaseSerializer(serializers.Serializer):
    name = serializers.CharField()
    nationality = serializers.CharField(required=False)


@extend_schema_serializer(examples=BOOK_BASE_SERIALIZER_EXAMPLES)
class BookBaseSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    isbn = serializers.CharField(max_length=17)
    title = serializers.CharField(max_length=200)
    author = AuthorBaseSerializer()
    genre = serializers.ChoiceField(choices=Book.GENRE_CHOICES)
    price = serializers.FloatField()
    stock_quantity = serializers.IntegerField()
    publication_date = serializers.DateField()
    tags = serializers.ListField(child=serializers.CharField())


class BookCreateInputSerializer(BookBaseSerializer):
    pass


class BookBaseOutputSerializer(BookBaseSerializer):
    pass
