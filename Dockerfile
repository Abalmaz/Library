FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY requirements.txt docker-entrypoint.sh /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /app
ENTRYPOINT  ["sh", "/app/docker-entrypoint.sh"]
EXPOSE 8000
