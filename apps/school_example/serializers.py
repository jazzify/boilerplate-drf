from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.school_example.docs.api import (
    SCHOOL_BASE_SERIALIZER_EXAMPLES,
    SCHOOL_NAMES_SERIALIZER_EXAMPLES,
)
from apps.school_example.models import School


@extend_schema_serializer(examples=SCHOOL_NAMES_SERIALIZER_EXAMPLES)
class SchoolCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class SchoolCreateFilterSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=False, default=False)


@extend_schema_serializer(examples=SCHOOL_BASE_SERIALIZER_EXAMPLES)
class SchoolBaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()


class SchoolOutputSerializer(SchoolBaseSerializer):
    pass
