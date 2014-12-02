FROM python:3.4

# Configure local
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install -r requirements/local.txt

EXPOSE 8000

CMD ["gunicorn", "-c", "tweetcheck/config/gunicorn_config.py", "wsgi:application"]
