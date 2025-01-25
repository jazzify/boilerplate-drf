from django.urls import path

from apps.school_example.apis import SchoolDetailDeleteApi, SchoolsListCreateApi

urlpatterns = [
    path("", SchoolsListCreateApi.as_view(), name="schools-list-create"),
    path("<int:pk>/", SchoolDetailDeleteApi.as_view(), name="schools-detail-delete"),
]
