FROM python:3.6.4
WORKDIR /usr/src/app
 
COPY requirements.txt ./
RUN apt-get install libxslt1-dev libxml2-dev &&\
    pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD [ "python", "./server.py" ]