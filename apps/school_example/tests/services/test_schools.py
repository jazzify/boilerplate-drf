from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from apps.school_example.models import School
from apps.school_example.services.schools import school_create


@pytest.mark.django_db
def test_school_create_success():
    school = school_create(name="Test School")
    assert school.name == "Test School"
    assert school.slug == "test-school"
    assert School.objects.filter(name="Test School").exists()


@pytest.mark.django_db
def test_school_create_with_custom_slug():
    school = school_create(name="Test School", custom_slug="custom-slug")
    assert school.name == "Test School"
    assert school.slug == "custom-slug"
    assert School.objects.filter(slug="custom-slug").exists()


@pytest.mark.django_db
def test_school_create_with_empty_name():
    with pytest.raises(ValidationError):
        school_create(name="")


@pytest.mark.django_db
def test_school_create_with_long_name():
    long_name = "A" * 256
    with pytest.raises(ValidationError):
        school_create(name=long_name)


@pytest.mark.django_db
def test_school_create_with_special_characters():
    special_name = "Test@School!"
    school = school_create(name=special_name)
    assert school.name == special_name
    assert school.slug == "testschool"
    assert School.objects.filter(name=special_name).exists()


@pytest.mark.django_db
@patch("apps.school_example.services.schools.slugify", return_value="test-school")
def test_school_create_slug_collision(mock_slugify):
    School.objects.create(name="Test School", slug="test-school")
    with pytest.raises(ValidationError):
        with patch(
            "apps.school_example.services.schools.uuid4", return_value="unique-id"
        ):
            school = school_create(name="Test School")
            assert school.slug == "Test School-unique-id"
            assert School.objects.filter(slug="Test School-unique-id").exists()
