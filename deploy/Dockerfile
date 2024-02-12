FROM python:3.9-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE=propertyDealsIn9ja.settings

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ../requirements.txt /app/
RUN pip install --upgrade pip --no-cache-dir && \
    pip install -r requirements.txt --no-cache-dir

# Copy the Django project files
COPY .. /app

# Collect static files (adjust as needed)
#RUN python manage.py collectstatic --noinput

# Create and apply database migrations (adjust as needed)
#RUN python manage.py migrate

# Expose the port that Daphne will run on
EXPOSE 8000

# Start Daphne as the entry point
#CMD ["daphne", "propertyDealsIn9ja.asgi:application", "--bind", "0.0.0.0:8000"]

#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "propertyDealsIn9ja.wsgi:application", "--bind", "0.0.0.0:8000"]

