import logging
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.template.defaultfilters import slugify

from apps.school_example.models import School

logger = logging.getLogger(__name__)


def school_active_list() -> QuerySet[School]:
    return School.objects.filter(is_active=True)


def school_create(name: str, custom_slug: str | None = None) -> School:
    retries = 3
    slug_name = slugify(name)
    while retries > 0:
        try:
            school_slug = custom_slug if custom_slug else slug_name
            school = School(name=name, slug=school_slug)
            school.validate_unique()
            school.full_clean()
            school.save()
            return school
        except ValidationError as e:
            if "slug" in e.message_dict:
                custom_slug = f"{slug_name}-{uuid4()}"
                retries -= 1
            else:
                logger.error(f"Failed to create school: {str(e)}")
                raise e
    raise ValidationError("Failed to create school after multiple retries")
