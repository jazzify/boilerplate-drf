from datetime import date
from typing import Optional

from django.db import transaction
from django.utils import timezone

from apps.school_example.models import School, Student
from apps.school_example.services.rosters import roster_create
from apps.school_example.services.school_courses import school_courses_list_by_school


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
