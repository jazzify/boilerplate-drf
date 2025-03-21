from datetime import date
from typing import Optional

from django.core.exceptions import ValidationError

from apps.school_example.constants import (
    ERROR_ROSTER_CREATE_DIFFERENT_SCHOOLS,
    ERROR_ROSTER_VALIDATE_PERIOD_OUTSIDE_COURSE_PERIOD,
)
from apps.school_example.models import Roster, SchoolCourse, Student


def roster_validate_period(
    *, start_date: date, end_date: date, school_course: SchoolCourse
) -> None:
    start_date_validation = (
        start_date >= school_course.start_date and start_date < school_course.end_date
    )

    end_date_validation = (
        end_date <= school_course.end_date
        and end_date > school_course.start_date
        and end_date > start_date
    )

    if not start_date_validation or not end_date_validation:
        raise ValidationError(
            ERROR_ROSTER_VALIDATE_PERIOD_OUTSIDE_COURSE_PERIOD.format(
                school_course=school_course
            )
        )


def roster_create(
    *,
    student: Student,
    school_course: SchoolCourse,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> Roster:
    if student.school != school_course.school:
        raise ValidationError(
            ERROR_ROSTER_CREATE_DIFFERENT_SCHOOLS.format(
                student=student, school_course=school_course
            )
        )
    start_date = start_date or school_course.start_date
    end_date = end_date or school_course.end_date

    roster_validate_period(
        start_date=start_date, end_date=end_date, school_course=school_course
    )

    roster = Roster(
        student=student,
        school_course=school_course,
        start_date=start_date,
        end_date=end_date,
    )
    roster.full_clean()
    roster.save()

    return roster
