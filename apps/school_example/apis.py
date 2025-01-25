from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.pagination import LimitOffsetPagination, get_paginated_response
from apps.school_example.serializers import (
    SchoolCreateInputSerializer,
    SchoolCreateOutputSerializer,
    SchoolListOutputSerializer,
)
from apps.school_example.services.schools import school_create, school_list


class SchoolsListCreateApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    @extend_schema(
        request=SchoolCreateInputSerializer,
        responses={status.HTTP_201_CREATED: SchoolCreateOutputSerializer},
    )
    def post(self, request):
        input_serializer = SchoolCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        school = school_create(name=input_serializer.validated_data["name"])
        return Response(
            data=SchoolCreateOutputSerializer(school).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses={status.HTTP_200_OK: SchoolListOutputSerializer},
    )
    def get(self, request):
        schools = school_list()
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=SchoolListOutputSerializer,
            queryset=schools,
            request=request,
            view=self,
        )
