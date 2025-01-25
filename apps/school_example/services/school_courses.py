from datetime import date
from typing import Optional

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from apps.school_example.models import School, SchoolCourse


def school_courses_list_by_school(
    *,
    school: School,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> QuerySet[SchoolCourse]:
    if end_date and not start_date:
        raise ValidationError("Start date must be provided when end date is provided")

    school_courses = school.school_courses.order_by("start_date")

    if start_date and not end_date:
        return school_courses.filter(start_date__gte=start_date)

    if start_date and end_date:
        return school_courses.filter(start_date__gte=start_date, end_date__lte=end_date)

    return school_courses
