# build stage
FROM python:3.8 AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY src/ /project/src
COPY .env /project/.env

# install dependencies and project into the local packages directory
WORKDIR /project
RUN pdm install

EXPOSE 8000

CMD ["pdm", "run", "dev"]
