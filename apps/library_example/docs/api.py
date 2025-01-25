from drf_spectacular.utils import OpenApiExample

BOOK_BASE_SERIALIZER_EXAMPLES = [
    OpenApiExample(
        "Book object example",
        value={
            "id": "67d473e2c50d4b6709d6df62",
            "isbn": "9782161484100",
            "title": "The Great Gatsby",
            "author": {
                "name": "F. Scott Fitzgerald",
            },
            "genre": "Classic",
            "price": 10.99,
            "stock_quantity": 50,
            "publication_date": "1925-04-10",
            "tags": ["Fiction", "Classic"],
        },
    ),
    OpenApiExample(
        "Book object example",
        value={
            "id": "67d382bce634b43d82543b96",
            "isbn": "978-3-16-148410-0",
            "title": "The Great Gatsby",
            "author": {
                "name": "F. Scott Fitzgerald",
                "nationality": "US",
            },
            "genre": "Classic",
            "price": 10.99,
            "stock_quantity": 50,
            "publication_date": "1925-04-10",
            "tags": ["Fiction", "Classic"],
        },
    ),
]
