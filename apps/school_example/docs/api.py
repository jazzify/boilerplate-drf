from drf_spectacular.utils import OpenApiExample

SCHOOL_NAMES_SERIALIZER_EXAMPLES = [
    OpenApiExample("School Names", value={"name": "Delta School"}),
    OpenApiExample("School Names", value={"name": "My High School"}),
]

SCHOOL_BASE_SERIALIZER_EXAMPLES = [
    OpenApiExample(
        "School Base Serializer",
        value={
            "id": 2,
            "name": "My High School",
            "slug": "my-high-school-4t9084da",
            "is_active": False,
        },
    ),
    OpenApiExample(
        "School Base Serializer",
        value={
            "id": 1,
            "name": "My High School",
            "slug": "my-high-school",
            "is_active": True,
        },
    ),
]
