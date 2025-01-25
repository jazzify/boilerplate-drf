from datetime import date
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.school_example.constants import (
    ERROR_SCHOOL_LIST_SCHOOL_COURSES_PROVIDE_START_DATE_MSG,
)
from apps.school_example.models import School, SchoolCourse, Student
from apps.school_example.services.rosters import roster_create


def school_courses_list_by_school(
    *,
    school: School,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> QuerySet[SchoolCourse]:
    if start_date is None and end_date:
        raise ValidationError(ERROR_SCHOOL_LIST_SCHOOL_COURSES_PROVIDE_START_DATE_MSG)

    school_courses = school.school_courses.order_by("start_date")

    if start_date and end_date:
        started_courses_Q = Q(
            start_date__lte=start_date, end_date__gte=start_date, end_date__lte=end_date
        )
        courses_in_period_q = Q(start_date__gte=start_date, end_date__lte=end_date)
        courses_wrapping_period_q = Q(
            start_date__lte=start_date, end_date__gte=end_date
        )
        future_course_q = Q(
            start_date__gte=start_date, start_date__lte=end_date, end_date__gte=end_date
        )

        return school_courses.filter(
            started_courses_Q
            | courses_in_period_q
            | courses_wrapping_period_q
            | future_course_q
        )

    if start_date and end_date is None:
        return school_courses.filter(
            Q(start_date__gte=start_date)
            | Q(start_date__lte=start_date, end_date__gte=start_date)
        )

    return school_courses


@transaction.atomic
def student_create(
    *, email: str, school: School, start_date: Optional[date] = None
) -> Student:
    student = Student(email=email, school=school)
    student.full_clean()
    student.save()

    start_date = start_date or timezone.now()

    school_courses = school_courses_list_by_school(school=school, start_date=start_date)

    for school_course in school_courses:
        roster_create(
            student=student,
            school_course=school_course,
            start_date=start_date,
            end_date=school_course.end_date,
        )

    return student


def school_list_school_courses(
    *,
    school: School,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> QuerySet[SchoolCourse]:
    if start_date is None and end_date:
        raise ValidationError(ERROR_SCHOOL_LIST_SCHOOL_COURSES_PROVIDE_START_DATE_MSG)

    school_courses = school.school_courses.order_by("start_date")

    if start_date and end_date:
        started_courses_Q = Q(
            start_date__lte=start_date, end_date__gte=start_date, end_date__lte=end_date
        )
        courses_in_period_q = Q(start_date__gte=start_date, end_date__lte=end_date)
        courses_wrapping_period_q = Q(
            start_date__lte=start_date, end_date__gte=end_date
        )
        future_course_q = Q(
            start_date__gte=start_date, start_date__lte=end_date, end_date__gte=end_date
        )

        return school_courses.filter(
            started_courses_Q
            | courses_in_period_q
            | courses_wrapping_period_q
            | future_course_q
        )

    if start_date and end_date is None:
        return school_courses.filter(
            Q(start_date__gte=start_date)
            | Q(start_date__lte=start_date, end_date__gte=start_date)
        )

    return school_courses
