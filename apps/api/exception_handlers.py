from typing import Any

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from mongoengine.errors import OperationError
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

from apps.api.exceptions import ApplicationError


def custom_exception_handler(exc: Exception, ctx: dict[str, Any]) -> Response | None:
    """
    {
        "message": "Error message",
        "extra": {}
    }
    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    # MongoDB Exceptions
    if isinstance(exc, OperationError):
        exc = exceptions.ValidationError(exc.args)

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {"message": exc.message, "extra": exc.extra}
            return Response(data, status=exc.status)
        return response

    if isinstance(exc.detail, (list, dict)):  # type: ignore
        response.data = {"detail": response.data}

    if response.data:
        if isinstance(exc, exceptions.ValidationError):
            response.data["message"] = "Validation error"
            response.data["extra"] = {"fields": response.data["detail"]}
        else:
            response.data["message"] = response.data["detail"]
            response.data["extra"] = {}

        del response.data["detail"]
    return response
