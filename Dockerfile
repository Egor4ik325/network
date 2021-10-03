# Base Docker image on Python 3 Docker image
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Move files to uniform location
COPY . /usr/src/app
WORKDIR /usr/src/app

# Install operating system dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev


# Install all dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Collect all static files (for serving)
RUN python manage.py collectstatic --no-input