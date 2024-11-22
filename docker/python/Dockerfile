FROM ${CI_DEPENDENCY_PROXY_DIRECT_GROUP_IMAGE_PREFIX}/python:${PYTHON_VERSION}-slim-bullseye

RUN apt-get update && \
    apt-get install -yqq \
        clang \
        curl \
        gcc \
        git \
        libcairo2 \
        libpq-dev \
        libsdl-pango-dev \
        make \
        postgresql-client \
        procps \
        python3-dev

COPY --from=ghcr.io/astral-sh/uv:${UV_VERSION} /uv /bin/uv

ENV DEBUG=true
ENV PYTHONUNBUFFERED=true
