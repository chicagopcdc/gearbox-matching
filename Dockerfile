ARG GIT_ACCESS_TOKEN

FROM quay.io/cdis/python:3.7-alpine as base

FROM base as builder
RUN apk add --no-cache --virtual .build-deps gcc g++ musl-dev libffi-dev openssl-dev make postgresql-dev git curl rust cargo 
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry --version 
RUN poetry self update --preview 
RUN poetry --version 
COPY . /src/
WORKDIR /src
# COPY . /tests/
# WORKDIR /tests
RUN git config --global user.name "stevekrasinsky" \
    && git config --global user.email "steve.krasinsky@gmail.com" \
    && git config --global url."https://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@github.com".insteadof "ssh://git@github.com"

RUN mkdir -p /env/src
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8
# RUN python -m venv /env && . /env/bin/activate && python -m pip install --upgrade pip && poetry -vvv install --no-interaction
RUN python -m venv /env 
RUN . /env/bin/activate 
RUN python -m pip install --upgrade pip 
RUN echo "NEXT STEP POETRY"
RUN pwd
RUN ls -a
RUN poetry -vvv install --no-interaction

FROM base
RUN apk add --no-cache postgresql-libs curl
COPY --from=builder /root/.poetry /root/.poetry
COPY --from=builder /env /env
COPY --from=builder /src /src
COPY --from=builder /tests /tests
ENV PATH="/env/bin/:${PATH}"
WORKDIR /src
CMD ["/env/bin/gunicorn", "gearbox.asgi:app", "-b", "0.0.0.0:80", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn.conf.py"]
