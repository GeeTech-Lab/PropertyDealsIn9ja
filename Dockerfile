FROM python:3.10
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt

# This will install the libpq-dev package which includes the pg_config
RUN apt-get update && apt-get install -y libpq-dev

RUN set -ex \
    # Runs pip commands and gets latest version of pip...
    && pip install --upgrade pip \
    # Install all from project requirements.txt to application requirements.txt
    && pip install --no-cache-dir -r /app/requirements.txt

# Working directory
WORKDIR /app

COPY . .

#====Defining connection port====
EXPOSE 8000

#====Running docker locally====
ENTRYPOINT ["gunicorn", "propertyDealsIn9ja.wsgi"]

##====Running docker locally====
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "propertyDealsIn9ja.wsgi:application"]

#====Running docker on heroku====
#CMD gunicorn propertyDealsIn9ja.wsgi:application --bind 0.0.0.0:$PORT
