FROM python:3.6-slim

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev libffi-dev nginx git supervisor libpcre3 libpcre3-dev --no-install-recommends && \
  rm -rf /var/lib/apt/lists/*

# install uwsgi, then uninstall the dependencies required to build it and run apt-get clean
RUN pip install uwsgi && apt-get remove -y build-essential libpq-dev libffi-dev && \
  apt-get clean && echo "daemon off;" >> /etc/nginx/nginx.conf

# setup all the configfiles
COPY /config/nginx-app.conf /etc/nginx/sites-available/default
COPY /config/supervisor-app.conf /etc/supervisor/conf.d/
COPY /config/uwsgi_params /config/uwsgi.ini /home/docker/code/

# copy projects
WORKDIR /home/docker/code/
COPY /app /home/docker/code/
RUN pip install -r requirements.txt

EXPOSE 80
CMD python manage.py collectstatic --noinput && python manage.py migrate && supervisord -n