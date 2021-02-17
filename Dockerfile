# FROM quay.io/cdis/ubuntu:18.04
FROM python:3.6-slim

# copy files app, uwsgi.ini, requirements.txt, start.sh
# COPY . /srv/flask_app
# WORKDIR /srv/flask_app

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

# Directory to check out editable projects into. The default in a virtualenv is “<venv path>/src”. The default for global installs is “<current dir>/src”.
# RUN pip install -r requirements.txt --src /usr/local/src

RUN mkdir client
# COPY --from=gear_front:test /app/build /client/build
COPY --from=quay.io/pcdc/gearbox_fe:master_Wed__17_Feb_2021_15_39_28_GMT /app/build /client/build

COPY start.sh .
COPY nginx.conf /etc/nginx/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN chmod +x ./start.sh
CMD ["./start.sh"]

# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]



