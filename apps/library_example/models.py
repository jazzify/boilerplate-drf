from django.utils import timezone
from mongoengine import (
    DateField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    ListField,
    StringField,
)


class Author(EmbeddedDocument):
    name = StringField(required=True)
    nationality = StringField()


class Book(Document):
    GENRE_CHOICES = [
        "Science Fiction",
        "Mystery",
        "Fantasy",
        "History",
        "Poetry",
        "Drama",
        "Thriller",
        "Romance",
        "Adventure",
        "Horror",
        "Comedy",
        "Action",
        "Crime",
    ]

    isbn = StringField(unique=True, max_length=17)
    title = StringField(required=True, max_length=200)
    author = EmbeddedDocumentField(Author)
    genre = StringField(choices=GENRE_CHOICES)
    price = FloatField(min_value=0)
    stock_quantity = IntField(min_value=0, default=0)
    publication_date = DateField()
    tags = ListField(StringField(), default=list)

    meta = {
        "collection": "book_inventory",
        "indexes": [
            "genre",
            "tags",
            ("author.name", "genre"),  # Compound index
        ],
    }


class SaleRecord(Document):
    book = StringField(required=True)  # ISBN or Book ID
    quantity_sold = IntField(required=True)
    total_revenue = FloatField(required=True)
    sale_performed_at = DateTimeField(default=timezone.now)

    meta = {
        "collection": "sales_records",
        "indexes": [
            "sale_performed_at",
            ("book", "-sale_performed_at"),  # Index on book and sale date
        ],
    }
