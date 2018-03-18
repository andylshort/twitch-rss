FROM python:3.6.4-alpine3.7
WORKDIR /app
ADD . /app
 
COPY requirements.txt ./
RUN apk upgrade --update && \
    apk add alpine-sdk libxml2-dev libxslt-dev && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD [ "python", "server.py" ]