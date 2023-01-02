FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN set -ex \
    # Runs pip commands and gets latest version of pip...
    && pip install --upgrade pip \
    # Install all from project requirements.txt to application requirements.txt
    && pip install --no-cache-dir -r /app/requirements.txt

ADD . .

#====Defining connection port====
#EXPOSE 8000

##====Running docker locally====
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "propertyDealsIn9ja.wsgi:application"]

#====Running docker on heroku====
#CMD gunicorn propertyDealsIn9ja.wsgi:application --bind 0.0.0.0:$PORT
CMD gunicorn propertyDealsIn9ja.wsgi --bind 0.0.0.0:$PORT