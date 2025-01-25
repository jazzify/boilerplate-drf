# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /code

# Set environment variables
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose port 8000
EXPOSE 8000

# Install system dependencies
## UV needs: curl (and certificates)
## MySQL needs: python3-dev default-libmysqlclient-dev build-essential pkg-config
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config

# Download the latest UV installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the UV installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --frozen --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /code
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENTRYPOINT []

# Run the Django application
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "django_project.wsgi:application"]
