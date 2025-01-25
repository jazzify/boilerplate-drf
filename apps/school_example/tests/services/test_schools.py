from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from apps.school_example.models import School
from apps.school_example.services.schools import school_active_list, school_create
from apps.school_example.tests.factories import SchoolFactory


@pytest.mark.django_db
def test_school_list_empty():
    assert school_active_list().count() == 0


@pytest.mark.django_db
def test_school_list_with_inactive_schools():
    SchoolFactory.create_batch(2)
    assert school_active_list().count() == 0


@pytest.mark.django_db
def test_school_list_with_active_schools():
    SchoolFactory.create_batch(2, is_active=True)
    assert school_active_list().count() == 2


@pytest.mark.django_db
def test_school_create_success():
    school = school_create(name="Test School")
    assert school.name == "Test School"
    assert school.slug == "test-school"
    assert School.objects.filter(name="Test School").exists()
    assert School.objects.all().count() == 1


@pytest.mark.django_db
def test_school_create_with_custom_slug():
    school = school_create(name="Test School", custom_slug="custom-slug")
    assert school.name == "Test School"
    assert school.slug == "custom-slug"
    assert School.objects.filter(slug="custom-slug").exists()


@pytest.mark.django_db
def test_school_create_with_empty_name():
    # Business rule:
    # We shouldn't be able to create a school with an empty name
    with pytest.raises(ValidationError):
        school_create(name="")


@pytest.mark.django_db
def test_school_create_with_long_name():
    # Business rule:
    # We shouldn't be able to create a school with a name longer than 255 characters
    long_name = "A" * 256
    with pytest.raises(ValidationError):
        school_create(name=long_name)


# WARNING: This is an abstract test example that contains the 2 tests above
# as an easy way to show how to use the pytest.mark.parametrize decorator
# to run the same test with different parameters.
@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_name",
    (
        "",  # empty name
        "A" * 256,  # name longer than 255 characters
    ),
)
def test_school_create_name_lengths(invalid_name):
    with pytest.raises(ValidationError):
        school_create(name=invalid_name)


@pytest.mark.django_db
def test_school_create_with_special_characters():
    # Business rule:
    # we should be able to create a school with special characters in the name
    special_name = "Test@School!"
    school = school_create(name=special_name)
    assert school.name == special_name
    assert school.slug == "testschool"
    assert School.objects.filter(name=special_name).exists()


@pytest.mark.django_db
def test_school_create_slug_collision():
    School.objects.create(name="Test School", slug="test-school")
    with patch("apps.school_example.services.schools.uuid4", return_value="1234"):
        school = school_create(name="Test School")
        assert school.slug == "test-school-1234"
        assert School.objects.filter(slug="test-school-1234").exists()
