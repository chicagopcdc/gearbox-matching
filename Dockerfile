ARG AZLINUX_BASE_VERSION=master

# Base stage with python-build-base
FROM quay.io/cdis/python-nginx-al:${AZLINUX_BASE_VERSION} AS base

ENV appname=gearbox

COPY --chown=gen3:gen3 /src/${appname} /${appname}

WORKDIR /${appname}

# Builder stage
FROM base AS builder

USER gen3

COPY poetry.lock pyproject.toml /${appname}/


# RUN python3 -m venv /env && . /env/bin/activate &&
RUN poetry install -vv --no-interaction --without dev

COPY --chown=gen3:gen3 . /${appname}
RUN chmod +x /${appname}/dockerrun.bash
COPY --chown=gen3:gen3 ./deployment/wsgi/wsgi.py /${appname}/wsgi.py

RUN poetry install -vv --no-interaction --without dev

ENV  PATH="$(poetry env info --path)/bin:$PATH"

# Final stage
FROM base

# Install ccrypt to decrypt dbgap telmetry files
RUN echo "Upgrading dnf"; \
    dnf upgrade -y; \
    echo "Installing Packages"; \
    dnf install -y \
        libxcrypt-compat-4.4.33 \
        libpq-15.0 \
        gcc \
        tar xz; \
    echo "Installing RPM"; \
    rpm -i https://ccrypt.sourceforge.net/download/1.11/ccrypt-1.11-1.src.rpm && \
    cd /root/rpmbuild/SOURCES/ && \
    tar -zxf ccrypt-1.11.tar.gz && cd ccrypt-1.11 && ./configure --disable-libcrypt && make install && make check;

COPY --from=builder /${appname} /${appname}

# Switch to non-root user 'gen3' for the serving process

USER gen3

CMD ["/bin/bash", "-c", "/${appname}/dockerrun.bash"]