# Base Docker image on Python 3 Docker image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Move files to uniform location
COPY . /usr/src/app
WORKDIR /usr/src/app

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]