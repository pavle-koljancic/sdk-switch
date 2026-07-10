FROM python:3.11-slim-bookworm AS python-base

ARG TEMP_DIR

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_INSTALLER_PARALLEL=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base AS builder-base
RUN apt update && \
    apt install --no-install-recommends -y \
        openssh-client \
        git


RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN pip3 install poetry==${POETRY_VERSION}

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
COPY ${TEMP_DIR} "${PYSETUP_PATH}"

RUN --mount=type=ssh poetry install --no-interaction --no-ansi -vvv --only main

FROM python-base AS production

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR "/home/app"
COPY "main.py" .
COPY workers ./workers
COPY workflows ./workflows

RUN mkdir -p docs
COPY ["changelog-worker.md", "."]
COPY ["docs", "./docs"]

CMD ["python3", "-u", "main.py"]
