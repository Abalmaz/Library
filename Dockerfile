FROM python:3.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
COPY docker-entrypoint.sh /app/
RUN chmod +x docker-entrypoint.sh
ADD . /app







