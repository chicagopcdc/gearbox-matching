FROM quay.io/cdis/python:3.7-alpine as base

FROM base as builder
RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev libffi-dev openssl-dev make postgresql-dev git curl rust cargo 
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
COPY . /src/
WORKDIR /src
COPY . /tests/
RUN python -m venv /env 
RUN . /env/bin/activate 
RUN python -m pip install --upgrade pip 
RUN poetry install -vvv --no-interaction

FROM base
RUN apk add --no-cache postgresql-libs curl
COPY --from=builder /env /env
COPY --from=builder /src /src
COPY --from=builder /tests /tests
ENV PATH="/env/bin/:${PATH}"
WORKDIR /src
CMD ["/env/bin/gunicorn", "gearbox.asgi:app", "-b", "0.0.0.0:80", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn.conf.py"]
