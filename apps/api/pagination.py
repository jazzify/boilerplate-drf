from collections import OrderedDict
from typing import Any, Type

from django.db.models import QuerySet
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework.pagination import (
    BasePagination,
)
from rest_framework.pagination import (
    LimitOffsetPagination as _LimitOffsetPagination,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_data(self, data: dict[str, Any]) -> OrderedDict[str, Any]:
        return OrderedDict(
            [
                ("limit", self.limit),
                ("offset", self.offset),
                ("count", self.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )

    def get_paginated_response(self, data: dict[str, Any]) -> Response:
        """
        We redefine this method in order to return `limit` and `offset`.
        This is used by the frontend to construct the pagination itself.
        """
        return Response(
            OrderedDict(
                [
                    ("limit", self.limit),
                    ("offset", self.offset),
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


def get_paginated_response(
    *,
    pagination_class: Type[BasePagination],
    serializer_class: Type[BaseSerializer],
    queryset: QuerySet[Any],
    request: Request,
    view: APIView,
) -> Response:
    paginator = pagination_class()
    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return Response(data=serializer.data)


def get_paginated_response_schema(
    schema: serializers.SerializerMetaclass,
) -> serializers.Serializer[Any]:
    return inline_serializer(
        name=f"PaginatedResponse{schema.__name__}",
        fields={
            "limit": serializers.IntegerField(),
            "offset": serializers.IntegerField(),
            "count": serializers.IntegerField(),
            "next": serializers.URLField(allow_null=True),
            "previous": serializers.URLField(allow_null=True),
            "results": schema(many=True),
        },
    )
