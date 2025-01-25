"""https://docs.djangoproject.com/en/5.1/topics/http/urls/"""

from django.conf import settings
from django.urls import include, path

#### Apps
urlpatterns = [
    path("api/", include("apps.api.urls")),
]

#### Django Debug Toolbar
if settings.DEBUG:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    ]
