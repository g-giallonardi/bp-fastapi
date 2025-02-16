FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    libpq-dev gcc build-essential

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt  \
    && pip install --force-reinstall --no-cache-dir bcrypt \
    && pip install --force-reinstall --no-cache-dir passlib


RUN python init_project.py fosslight

EXPOSE 8000