from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError
from django.http import Http404

from apps.school_example.models import School
from apps.school_example.services.schools import (
    school_active_list,
    school_create,
    school_delete,
    school_retrieve,
)
from apps.school_example.tests.factories import SchoolFactory


@pytest.mark.django_db
class TestSchoolDelete:
    @pytest.mark.parametrize(
        "is_active",
        [
            True,
            False,
        ],
    )
    def test_delete_existing_school(self, is_active):
        school = School.objects.create(name="Test School", is_active=is_active)
        school_pk = school.pk
        school_delete(school_pk)
        updated_school = School.objects.get(pk=school_pk)

        assert not updated_school.is_active

    def test_delete_non_existent_school(self):
        with pytest.raises(Http404):
            school_delete(999)


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


# WARNING: This is a "dynamic params" test example that contains the 2 tests above
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


@pytest.mark.parametrize("is_active, expected", [(True, True), (False, False)])
@pytest.mark.django_db
def test_school_create_with_is_active(is_active, expected):
    school = school_create(name="Test School", is_active=is_active)
    assert school.is_active == expected


@pytest.mark.django_db
def test_school_retrieve_exists():
    school = School.objects.create(name="Test School")
    retrieved_school = school_retrieve(school.pk)
    assert retrieved_school == school


@pytest.mark.django_db
def test_school_retrieve_not_exists():
    with pytest.raises(Http404):
        school_retrieve(1)
