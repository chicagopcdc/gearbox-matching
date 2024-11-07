FROM quay.io/cdis/python:python3.9-buster-2.0.0 AS base

FROM base AS builder
RUN pip install --upgrade pip

RUN pip install poetry

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential gcc make musl-dev libffi-dev libssl-dev git curl bash
COPY . /src/
WORKDIR /src

RUN mkdir src/gearbox/keys/

RUN poetry lock

RUN python -m venv /env && . /env/bin/activate && poetry install --no-interaction --no-dev


FROM base
COPY --from=builder /env /env
COPY --from=builder /src /src
ENV PATH="/env/bin/:${PATH}"
WORKDIR /src
CMD ["/env/bin/gunicorn", "gearbox.asgi:app", "-b", "0.0.0.0:80", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn.conf.py"]
