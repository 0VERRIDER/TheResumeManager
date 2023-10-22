FROM python:3.11

RUN apt install python3 -y
RUN apt install python3.11-venv -y
RUN curl -sSL https://pdm.fming.dev/install-pdm.py | python3 -

RUN mkdir /app

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml
COPY ./pdm.lock /app/pdm.lock

COPY . /app/

RUN pdm install

CMD ["pdm", "run", "start"]
