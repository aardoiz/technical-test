FROM python:3.12-bookworm as base

ENV USERNAME "python"
ENV APP_HOME "/home/$USERNAME"
ENV APP_PATH "$APP_HOME/code"

ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.8.3
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

ARG uid=1000
ARG gid=1000

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=DL3008
RUN apt-get -y update \
    && apt-get -y install git curl make --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -g "$gid" "$USERNAME" \
    && useradd -lu "$uid" -g "$gid" "$USERNAME" \
    && mkhomedir_helper "$USERNAME" \
    && mkdir "$APP_PATH" \
    && chown "$uid:$gid" "$APP_PATH"


USER "$USERNAME"
ENV PATH="${PATH}:$APP_HOME/.local/bin"
ENV PYTHONPATH "$APP_PATH"

RUN pip install --upgrade pip==24.0 pipx==1.5.0 --no-cache-dir \
    && pipx install poetry==$POETRY_VERSION \
    && pipx install pre-commit==3.7.1

WORKDIR "$APP_PATH"

FROM base as run
COPY --chown="$USERNAME" pyproject.toml poetry.lock README.md Makefile ./

RUN poetry install --no-cache --no-interaction --no-ansi

COPY --chown="$USERNAME" . ./

CMD ["poetry", "run", "uvicorn", "apps.ai_chat.http.app:app", "--host", "0.0.0.0", "--port", "8000"]
