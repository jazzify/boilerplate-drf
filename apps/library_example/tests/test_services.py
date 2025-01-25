from apps.common.tests import faker
from apps.library_example.models import Author, Book
from apps.library_example.services import book_create, get_all_active_books
from apps.library_example.tests.factories import BookFactory


def test_book_create():
    isbn = faker.isbn13().replace("-", "")
    author = Author(
        name=faker.unique.name(),
        nationality=faker.unique.country_code(),
    )

    book = book_create(
        isbn=isbn,
        title=faker.unique.company(),
        author=author,
        genre="Science Fiction",
        price=9.99,
        stock_quantity=10,
        publication_date="2022-01-01",
        tags=["test", "book"],
    )
    assert book.isbn == isbn
    assert book.author == author
    assert book.genre == "Science Fiction"
    assert book.price == 9.99
    assert book.stock_quantity == 10
    assert book.publication_date == "2022-01-01"
    assert book.tags == ["test", "book"]


def test_get_all_active_books():
    non_stocked_books = BookFactory.build_batch(size=3, stock_quantity=0)
    stocked_books = BookFactory.build_batch(size=3)
    all_books = non_stocked_books + stocked_books

    Book.objects.insert(all_books)
    result = get_all_active_books()
    assert len(result) == 3
