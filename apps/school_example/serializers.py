from rest_framework import serializers

from apps.school_example.models import School


class SchoolCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class SchoolCreateFilterSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=False, default=False)


class SchoolBaseOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()


class SchoolListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("id", "name", "slug")
