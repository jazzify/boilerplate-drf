from rest_framework import serializers

from apps.school_example.models import School


class SchoolCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class SchoolCreateOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.CharField(max_length=255)


class SchoolListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ("id", "name", "slug")
