FROM python:3.11

RUN pip install pdm

RUN export PATH=/root/.local/bin:$PATH

RUN mkdir /app

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml
COPY ./pdm.lock /app/pdm.lock

COPY . /app/

RUN pdm install

CMD ["pdm", "run", "dev"]
