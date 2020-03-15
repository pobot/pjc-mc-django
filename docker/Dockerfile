FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .

RUN pip install pip -U \
    && pip install -r requirements.txt

RUN useradd -u 1000 pjcmc
USER pjcmc

ENTRYPOINT ["/app/docker-entrypoint.sh"]

COPY . .
