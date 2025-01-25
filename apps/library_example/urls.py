from django.urls import path

from apps.library_example.apis import BookListCreateApi

urlpatterns = [
    path("books/", BookListCreateApi.as_view(), name="books-list-create"),
]
