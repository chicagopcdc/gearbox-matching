FROM quay.io/cdis/python:python3.9-buster-2.0.0 AS base

FROM base AS builder

# PATCH: Point to archived Debian Buster repositories
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential gcc make musl-dev libffi-dev libssl-dev git curl bash

RUN pip install --upgrade pip

RUN pip install poetry

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential gcc make musl-dev libffi-dev libssl-dev git curl bash
COPY . /src/
WORKDIR /src

RUN mkdir src/gearbox/keys/

RUN poetry lock

RUN python -m venv /env && . /env/bin/activate && poetry install --no-interaction --without dev
# OR RUN python -m venv /env && . /env/bin/activate && poetry install --only main --no-interaction

FROM base
COPY --from=builder /env /env
COPY --from=builder /src /src
ENV PATH="/env/bin/:${PATH}"
WORKDIR /src
CMD ["/env/bin/gunicorn", "gearbox.asgi:app", "-b", "0.0.0.0:80", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn.conf.py"]
