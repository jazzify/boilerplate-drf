from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
    get_paginated_response_schema,
)
from apps.library_example.docs.api import BOOK_BASE_SERIALIZER_EXAMPLES
from apps.library_example.models import Author
from apps.library_example.serializers import (
    BookBaseOutputSerializer,
    BookCreateInputSerializer,
)
from apps.library_example.services import book_create, get_all_active_books


@extend_schema_view(
    post=extend_schema(
        summary="Books Create",
        request=BookCreateInputSerializer,
        responses={status.HTTP_201_CREATED: BookBaseOutputSerializer},
    ),
    get=extend_schema(
        summary="Books List",
        responses={
            status.HTTP_201_CREATED: get_paginated_response_schema(
                BookBaseOutputSerializer, examples=BOOK_BASE_SERIALIZER_EXAMPLES
            )
        },
    ),
)
class BookListCreateApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    def post(self, request: Request) -> Response:
        """
        > We use to charge for book creation, but now we don't.
        >    - Now: Free!
        >    - Before: $~~0.99~~

        Create a new book instance with a given `ISBN`, `title`, `author`,
        `genre`, `price`, `stock_quantity`, `publication_date` and `tags`.

        - Author is created if not exists.
        - Also author's `nationality` is optional.

        #### Author object example:
        ```
        "author": {
            "name": "F. Scott Fitzgerald",
            "nationality": "US" # optional
        }
        ```

        for a more detailed explanation of MD [click here.](https://es.wikipedia.org/wiki/Markdown)
        """
        input_serializer = BookCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_author_serializer = input_serializer.validated_data["author"]

        author = Author(
            name=input_author_serializer.get("name"),
            nationality=input_author_serializer.get("nationality", None),
        )
        book = book_create(
            isbn=input_serializer.validated_data["isbn"],
            title=input_serializer.validated_data["title"],
            author=author,
            genre=input_serializer.validated_data["genre"],
            price=input_serializer.validated_data["price"],
            stock_quantity=input_serializer.validated_data["stock_quantity"],
            publication_date=input_serializer.validated_data["publication_date"],
            tags=input_serializer.validated_data["tags"],
        )

        return Response(
            status=status.HTTP_201_CREATED, data=BookBaseOutputSerializer(book).data
        )

    def get(self, request: Request) -> Response:
        """
        Retrieves a paginated list of books in the library
        """
        books = get_all_active_books()

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=BookBaseOutputSerializer,
            queryset=books,
            request=request,
            view=self,
        )
