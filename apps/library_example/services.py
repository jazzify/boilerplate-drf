from apps.library_example.models import Author, Book


def book_create(
    isbn: str,
    title: str,
    author: Author,
    genre: str,
    price: float,
    stock_quantity: int,
    publication_date: str,
    tags: list[str],
) -> Book:
    book = Book(
        isbn=isbn,
        title=title,
        author=author,
        genre=genre,
        price=price,
        stock_quantity=stock_quantity,
        publication_date=publication_date,
        tags=tags,
    )
    book.save()

    return book


def get_all_active_books() -> list[Book]:
    return Book.objects(stock_quantity__gt=0)  # type: ignore[no-any-return]
