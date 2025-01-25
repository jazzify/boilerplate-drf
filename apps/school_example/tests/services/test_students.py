from unittest.mock import patch

import pytest

from apps.common.tests import faker
from apps.school_example.services.students import student_create
from apps.school_example.tests.factories import SchoolCourseFactory, SchoolFactory


@pytest.mark.django_db
@patch("apps.school_example.services.students.school_courses_list_by_school")
@patch("apps.school_example.services.students.roster_create")
class TestStudentCreate:
    def test_student_create(self, roster_create_mock, school_courses_mock):
        email = faker.unique.email()
        school = SchoolFactory()
        school_courses_mock.return_value = SchoolCourseFactory.stub_batch(size=5)

        student = student_create(email=email, school=school)

        assert student.email == email
        assert student.school == school
        assert student.identifier is not None

    def test_student_create_with_start_date(
        self, roster_create_mock, school_courses_mock
    ):
        school = SchoolFactory()
        SchoolCourseFactory.create_batch(5, school=school)
        email = faker.unique.email()
        start_date = faker.date_object()

        student = student_create(email=email, school=school, start_date=start_date)

        for school_course in school_courses_mock.return_value:
            roster_create_mock.assert_called_with(
                student=student,
                school_course=school_course,
                start_date=start_date,
                end_date=school_course.end_date,
            )
        school_courses_mock.assert_called_with(school=school, start_date=start_date)
