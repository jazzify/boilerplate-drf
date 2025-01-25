from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
    get_paginated_response_schema,
)
from apps.api.serializers import BaseErrorSerializer
from apps.school_example.docs.api import SCHOOL_BASE_SERIALIZER_EXAMPLES
from apps.school_example.serializers import (
    SchoolCreateFilterSerializer,
    SchoolCreateInputSerializer,
    SchoolOutputSerializer,
)
from apps.school_example.services.schools import (
    school_active_list,
    school_create,
    school_delete,
    school_retrieve,
)


class SchoolsListCreateApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    @extend_schema(
        summary="School Create API",
        parameters=[SchoolCreateFilterSerializer],
        request=SchoolCreateInputSerializer,
        responses={status.HTTP_201_CREATED: SchoolOutputSerializer},
    )
    def post(self, request: Request) -> Response:
        filters_serializer = SchoolCreateFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        input_serializer = SchoolCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        school = school_create(
            name=input_serializer.validated_data["name"],
            is_active=filters_serializer.validated_data["is_active"],
        )
        return Response(
            data=SchoolOutputSerializer(school).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="School List API",
        responses={
            status.HTTP_200_OK: get_paginated_response_schema(
                SchoolOutputSerializer, examples=SCHOOL_BASE_SERIALIZER_EXAMPLES
            )
        },
    )
    def get(self, request: Request) -> Response:
        schools = school_active_list()
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=SchoolOutputSerializer,
            queryset=schools,
            request=request,
            view=self,
        )


class SchoolDetailDeleteApi(APIView):
    @extend_schema(
        summary="School Detail API",
        responses={
            status.HTTP_201_CREATED: SchoolOutputSerializer,
            status.HTTP_404_NOT_FOUND: BaseErrorSerializer,
        },
    )
    def get(self, request: Request, pk: int) -> Response:
        school = school_retrieve(school_pk=pk)
        return Response(
            data=SchoolOutputSerializer(school).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="School Delete API",
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: BaseErrorSerializer,
        },
    )
    def delete(self, request: Request, pk: int) -> Response:
        school_delete(school_pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
