FROM python:3.7-stretch

WORKDIR /usr/src/python_exercice/

RUN adduser --disabled-password --gecos '' celery_user

COPY setup.py /usr/src/python_exercice/setup.py
COPY . /usr/src/python_exercice
RUN cd /usr/src/python_exercice && python setup.py develop
CMD ["django-admin migrate && django-admin runserver 0.0.0.0:8000"]