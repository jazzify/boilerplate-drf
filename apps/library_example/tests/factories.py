import factory

from apps.common.tests import faker
from apps.library_example.models import Author, Book


class AuthorFactory(factory.base.Factory):
    class Meta:
        model = Author

    name = factory.LazyAttribute(lambda _: faker.unique.name())
    nationality = factory.LazyAttribute(lambda _: faker.unique.country_code())


class BookFactory(factory.base.Factory):
    class Meta:
        model = Book

    isbn = factory.LazyAttribute(lambda _: faker.isbn13().replace("-", ""))
    title = factory.LazyAttribute(lambda _: faker.unique.company())
    author = factory.SubFactory(AuthorFactory)
    genre = factory.Iterator(Book.GENRE_CHOICES)
    price = faker.pyfloat(left_digits=2, right_digits=2, positive=True)
    stock_quantity = faker.pyint(min_value=1, max_value=10)
    publication_date = faker.past_date()
    tags = faker.words(nb=faker.pyint(min_value=1, max_value=3))
