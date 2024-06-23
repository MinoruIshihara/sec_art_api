FROM python:3.12-bullseye

WORKDIR /sec_art_api

COPY source/Pipfile /sec_art_api/
RUN pip install pipenv --no-cache-dir && \
    pipenv install

EXPOSE 8080