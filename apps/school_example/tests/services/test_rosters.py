from datetime import timedelta
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.school_example.constants import (
    ERROR_ROSTER_CREATE_DIFFERENT_SCHOOLS,
    ERROR_ROSTER_VALIDATE_PERIOD_OUTSIDE_COURSE_PERIOD,
)
from apps.school_example.models import Roster
from apps.school_example.services.rosters import roster_create, roster_validate_period
from apps.school_example.tests.factories import SchoolCourseFactory, StudentFactory


class RosterCreateTests(TestCase):
    def test_service_raises_error_if_different_schools(self):
        school_course = SchoolCourseFactory.build()
        student = StudentFactory.build()

        with self.assertRaisesMessage(
            ValidationError,
            ERROR_ROSTER_CREATE_DIFFERENT_SCHOOLS.format(
                student=student, school_course=school_course
            ),
        ):
            roster_create(student=student, school_course=school_course)

        self.assertEqual(Roster.objects.count(), 0)

    @patch("apps.school_example.services.rosters.roster_validate_period")
    def test_service_does_not_create_roster_if_period_is_not_valid(
        self, roster_validate_period_mock
    ):
        roster_validate_period_mock.side_effect = ValidationError("")

        school_course = SchoolCourseFactory.build()
        student = StudentFactory.build()

        with self.assertRaises(ValidationError):
            roster_create(student=student, school_course=school_course)

        self.assertEqual(Roster.objects.count(), 0)

    @patch("apps.school_example.services.rosters.roster_validate_period")
    def test_service_uses_school_course_period_for_default_period(
        self, roster_validate_period_mock
    ):
        school_course = SchoolCourseFactory()
        student = StudentFactory(school=school_course.school)

        roster = roster_create(student=student, school_course=school_course)

        self.assertEqual(roster.start_date, school_course.start_date)
        self.assertEqual(roster.end_date, school_course.end_date)

    @patch("apps.school_example.services.rosters.roster_validate_period")
    def test_service_doesn_not_school_course_period_if_dates_are_passed(
        self, roster_validate_period_mock
    ):
        school_course = SchoolCourseFactory()
        student = StudentFactory(school=school_course.school)

        start_date = timezone.now().date()
        end_date = school_course.end_date - timedelta(days=1)

        roster = roster_create(
            student=student,
            school_course=school_course,
            start_date=start_date,
            end_date=end_date,
        )

        self.assertEqual(roster.start_date, start_date)
        self.assertEqual(roster.end_date, end_date)


class RosterValidatePeriodTests(TestCase):
    def test_service_does_not_raise_error_if_valid_period(self):
        course = SchoolCourseFactory.build()

        roster_period_equal_to_course_period = {
            "start_date": course.start_date,
            "end_date": course.end_date,
        }
        roster_period_inside_course_period = {
            "start_date": course.start_date + timedelta(days=1),
            "end_date": course.end_date - timedelta(days=1),
        }
        roster_period_end_inside_course_period = {
            "start_date": course.start_date,
            "end_date": course.end_date - timedelta(days=1),
        }
        roster_period_start_inside_course_period = {
            "start_date": course.start_date + timedelta(days=1),
            "end_date": course.end_date,
        }

        roster_validate_period(
            school_course=course, **roster_period_equal_to_course_period
        )
        roster_validate_period(
            school_course=course, **roster_period_inside_course_period
        )
        roster_validate_period(
            school_course=course, **roster_period_end_inside_course_period
        )
        roster_validate_period(
            school_course=course, **roster_period_start_inside_course_period
        )

    def test_services_raises_error_for_rosters_outside_period(self):
        course = SchoolCourseFactory.build()

        roster_period_end_before_course_start = {
            "start_date": course.start_date - timedelta(days=10),
            "end_date": course.start_date - timedelta(days=5),
        }
        roster_period_start_before_course_start = {
            "start_date": course.start_date - timedelta(days=10),
            "end_date": course.start_date + timedelta(days=1),
        }
        roster_period_start_after_course_end = {
            "start_date": course.end_date + timedelta(days=5),
            "end_date": course.end_date + timedelta(days=10),
        }
        roster_period_end_after_course_end = {
            "start_date": course.end_date - timedelta(days=1),
            "end_date": course.end_date + timedelta(days=10),
        }

        for roster_period in [
            roster_period_end_before_course_start,
            roster_period_start_before_course_start,
            roster_period_start_after_course_end,
            roster_period_end_after_course_end,
        ]:
            with self.assertRaisesMessage(
                ValidationError,
                ERROR_ROSTER_VALIDATE_PERIOD_OUTSIDE_COURSE_PERIOD.format(
                    school_course=course
                ),
            ):
                roster_validate_period(school_course=course, **roster_period)
