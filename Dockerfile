FROM python:3.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY requirements.txt docker-entrypoint.sh /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN chmod +x /app/docker-entrypoint.sh
ADD . /app
ENTRYPOINT  ["/app/docker-entrypoint.sh"]
EXPOSE 8000









