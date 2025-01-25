from datetime import datetime, timedelta

import pytest

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
