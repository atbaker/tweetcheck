FROM python:2.7.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install -r requirements/local.txt

EXPOSE 8000

CMD [ "python", "twitter-approver/manage.py", "runserver", "0.0.0.0:8000"]
