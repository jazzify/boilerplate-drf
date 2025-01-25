_PROJECT_DESCRIPTION = """
A modern Django REST framework boilerplate with MongoDB and MySQL integration.

#### Response Headers:
- `X-Request-ID`: A unique request ID generated for each request.
"""

# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    "TITLE": "Django Boilerplate API",
    "DESCRIPTION": _PROJECT_DESCRIPTION,
    "VERSION": "0.1.0",
    "OAS_VERSION": "3.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "REDOC_DIST": "SIDECAR",
    # https://redocly.com/docs/redoc/config/#functional-settings
    # The settings are serialized with json.dumps(). If you need customized JS, use a
    # string instead. The string must then contain valid JS and is passed unchanged.
    "REDOC_UI_SETTINGS": {
        "theme": {
            "sidebar": {
                "backgroundColor": "#255994",
                "textColor": "#F5F5F5",
            },
            "rightPanel": {
                "backgroundColor": "#002855",
                "textColor": "#F5F5F5",
            },
        }
    },
}
