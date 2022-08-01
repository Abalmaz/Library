FROM python:3.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
ADD requirements.txt docker-entrypoint.sh /app/
RUN pip install -r requirements.txt && chmod +x docker-entrypoint.sh
ADD . /app

# start server
EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/app/docker-entrypoint.sh"]








