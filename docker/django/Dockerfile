FROM python:3.8.6 as base
COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.8.6-slim as build

LABEL maintainer="rodrigo@local"
LABEL vendor="rodrigo"

# Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PYTHONBREAKPOINT=ipdb.set_trace

# Pip
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 100

# Django
ENV DJANGO_SETTINGS_MODULE api.settings
ENV TZ America/Sao_Paulo

RUN apt-get update && apt-get install -y --no-install-recommends gettext

COPY --from=base /root/.cache /root/.cache
COPY --from=base requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN rm -rf /root/.cache

COPY ./docker/django/runserver.sh /runserver.sh
RUN chmod +x "/runserver.sh"

WORKDIR /usr/src/app

COPY api /usr/src/app

USER 1000

CMD ["/runserver.sh"]
