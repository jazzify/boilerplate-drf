from django.urls import path

from apps.school_example.apis import (
    SchoolsListCreateApi,
)

urlpatterns = [
    path("", SchoolsListCreateApi.as_view(), name="schools"),
]
