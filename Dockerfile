ARG AZLINUX_BASE_VERSION=3.13-pythonnginx

# Base stage with python-build-base
FROM quay.io/cdis/amazonlinux-base:${AZLINUX_BASE_VERSION} AS base

ENV appname=gearbox

COPY --chown=gen3:gen3 /src/${appname} /${appname}

WORKDIR /${appname}

# Builder stage
FROM base AS builder

USER root
# git is required by build.py (clones gearboxdatamodel migrations).
# Install it here explicitly in case the base image does not include it.
RUN dnf install -y git && chown -R gen3:gen3 /venv

USER gen3

# Copy only the files needed to resolve and install dependencies so that
# this layer is cached independently of source-code changes.
COPY poetry.lock pyproject.toml /${appname}/

# Install all dependencies but skip the root package (--no-root) so that
# the build hook (build.py) is not invoked here.  This gives us a fast,
# cacheable layer that only reruns when poetry.lock or pyproject.toml change.
RUN poetry install -vv --no-interaction --without dev --no-root

# Copy the full source tree (including build.py).
COPY --chown=gen3:gen3 . /${appname}
RUN chmod +x /${appname}/dockerrun.bash
COPY --chown=gen3:gen3 ./deployment/wsgi/wsgi.py /${appname}/wsgi.py

# Fetch migrations once, explicitly and cleanly.
RUN python build.py

# Install the root package.  build.py's ref-marker check makes this a no-op
# for the git-clone step if migrations/ is already populated.
RUN poetry install -vv --no-interaction --without dev

ENV  PATH="$(poetry env info --path)/bin:$PATH"

# Final stage
FROM base

USER root

# Install ccrypt to decrypt dbgap telmetry files
RUN echo "Upgrading dnf"; \
    dnf upgrade -y; \
    echo "Installing Packages"; \
    dnf install -y \
        libxcrypt-compat-4.4.33 \
        libpq-15.0 \
        gcc \
        diffutils \
        tar xz; \
    echo "Installing RPM"; \
    rpm -i https://ccrypt.sourceforge.net/download/1.11/ccrypt-1.11-1.src.rpm && \
    cd /root/rpmbuild/SOURCES/ && \
    tar -zxf ccrypt-1.11.tar.gz && cd ccrypt-1.11 && ./configure --disable-libcrypt && make install && make check;

COPY --from=builder /${appname} /${appname}
COPY --from=builder /venv /venv

# Switch to non-root user 'gen3' for the serving process

USER gen3

CMD ["/bin/bash", "-c", "/${appname}/dockerrun.bash"]
