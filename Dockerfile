FROM python:3.4

# Configure local
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install requirements
RUN mkdir /usr/src/app/requirements
COPY ./requirements /usr/src/app/requirements
RUN pip install -r requirements/local.txt

COPY . /usr/src/app

# Run collectstatic
RUN python tweetcheck/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "-c", "tweetcheck/config/gunicorn_config.py", "wsgi:application"]
