#!/bin/bash

nginx
poetry run gunicorn -c "/gearbox/deployment/wsgi/gunicorn.conf.py" gearbox.asgi:app