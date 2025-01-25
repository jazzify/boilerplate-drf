import logging
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify

from apps.school_example.models import School

logger = logging.getLogger(__name__)


def school_active_list() -> QuerySet[School]:
    return School.objects.filter(is_active=True)


def school_create(
    name: str, custom_slug: str | None = None, is_active: bool = False
) -> School:
    """
    Creates a new School instance with the given name and an optional custom slug.

    If a custom slug is not provided, a slugified version of the name will be used.
    The function will attempt to create the school up to 3 times if there are slug
    conflicts, appending a UUID segment to the slug each time a conflict occurs.

    Args:
        name (str): The name of the school to be created.
        custom_slug (str | None, optional): A custom slug for the school. Defaults to None.

    Returns:
        School: The created School instance.

    Raises:
        ValidationError: If the school cannot be created after multiple retries or if
                        there are other validation errors.
    """
    retries = 3
    slug_name = custom_slug if custom_slug else slugify(name)
    while retries > 0:
        try:
            school = School(name=name, slug=slug_name, is_active=is_active)
            school.full_clean()
            school.save()
            return school
        except ValidationError as e:
            if "slug" in e.message_dict:
                slug_name = f"{slug_name}-{str(uuid4())[0:8]}"
                retries -= 1
            else:
                raise e
    logger.error(f"Failed to create school with: {name=} and {custom_slug=}")
    raise ValidationError("Failed to create school after multiple retries")


def school_delete(school_pk: int) -> None:
    """Sets the School instance with the given primary key as inactive.

    Args:
        school_pk (int): The primary key of the School instance to be deleted.

    Raises:
        Http404: If the School instance with the given primary key does not exist.

    """
    school = get_object_or_404(School, pk=school_pk)
    school.is_active = False
    school.save()
    logger.info(f"Deleted school with pk: {school_pk}")


def school_retrieve(school_pk: int) -> School:
    return get_object_or_404(School, pk=school_pk)
