from datetime import datetime, timedelta

import pytest
from django.core.exceptions import ValidationError

from apps.school_example.services.school_courses import school_courses_list_by_school
from apps.school_example.tests.factories import SchoolCourseFactory, SchoolFactory


@pytest.mark.django_db
def test_school_courses_list_by_school():
    school = SchoolFactory()
    school_courses_factory = SchoolCourseFactory.create_batch(2, school=school)
    school_courses = school_courses_list_by_school(school=school)

    for course in school_courses:
        assert course.school == school
        assert course in school_courses_factory


@pytest.mark.django_db
def test_school_courses_list_by_school_with_start_date():
    school = SchoolFactory()
    start_date = datetime.now().date()

    SchoolCourseFactory.create_batch(
        2, school=school, start_date=start_date - timedelta(days=1)
    )
    updated_courses = SchoolCourseFactory.create_batch(
        2, school=school, start_date=start_date + timedelta(days=1)
    )

    school_courses = school_courses_list_by_school(school=school, start_date=start_date)

    assert school_courses.count() == 2
    for course in school_courses:
        assert course in updated_courses


@pytest.mark.django_db
def test_school_courses_list_by_school_with_start_and_end_date():
    school = SchoolFactory()
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=10)

    SchoolCourseFactory.create_batch(
        2, school=school, start_date=start_date - timedelta(days=1)
    )
    SchoolCourseFactory.create_batch(
        2, school=school, start_date=end_date + timedelta(days=1)
    )
    valid_courses = SchoolCourseFactory.create_batch(
        2,
        school=school,
        start_date=start_date + timedelta(days=1),
        end_date=end_date - timedelta(days=1),
    )

    school_courses = school_courses_list_by_school(
        school=school, start_date=start_date, end_date=end_date
    )

    assert school_courses.count() == 2
    for course in school_courses:
        assert course in valid_courses


@pytest.mark.django_db
def test_school_courses_list_by_school_with_end_date_only():
    school = SchoolFactory()
    end_date = datetime.now().date() + timedelta(days=10)

    with pytest.raises(ValidationError):
        school_courses_list_by_school(school=school, end_date=end_date)
