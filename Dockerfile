FROM python:3.9-slim
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["gunicorn", "legacy_kitchen_lounge.wsgi"]

##====Running docker locally====
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "propertyDealsIn9ja.wsgi:application"]

#====Running docker on heroku====
#CMD gunicorn propertyDealsIn9ja.wsgi:application --bind 0.0.0.0:$PORT
