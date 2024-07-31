FROM python:3.12-slim-bullseye as base

ENV USERNAME=python
ENV APP_HOME=/home/python
ENV APP_PATH=/home/python/code

ENV POETRY_VERSION=1.8.3
ENV PATH="${APP_HOME}/.local/bin:${PATH}"
ENV PYTHONPATH="${APP_PATH}"

ARG uid=1000
ARG gid=1000

RUN apt-get update \
    && apt-get -y install git curl --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -g "${gid}" "${USERNAME}" \
    && useradd -m -l -u "${uid}" -g "${gid}" -d "${APP_HOME}" "${USERNAME}" \
    && mkdir -p "${APP_PATH}" \
    && chown "${uid}:${gid}" "${APP_PATH}"

USER "${USERNAME}"

RUN pip install --no-cache-dir pip==24.0 pipx==1.5.0 \
    && pipx install poetry==${POETRY_VERSION} \
    && pipx install pre-commit==3.7.1

WORKDIR "${APP_PATH}"

FROM base as run

COPY --chown="${USERNAME}" pyproject.toml poetry.lock README.md Makefile ./

RUN poetry install --no-interaction --no-root

COPY --chown="${USERNAME}" . ./

CMD ["poetry", "run", "uvicorn", "apps.chat.http.app:app", "--host", "0.0.0.0", "--port", "8000"]
