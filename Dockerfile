FROM python:3.12.2-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /
RUN apt-get update \
    && apt-get install -y \
        gcc \
        libffi-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD [ "python", "run.py" ]