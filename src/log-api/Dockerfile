FROM ubuntu:trusty

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
 python-pip \
 python-dev

RUN pip install -r requirements.txt

COPY rainbowfs rainbowfs
COPY app.py .

ENV PYTHONPATH=/usr/src/app

ENTRYPOINT [ "python", "-u", "./app.py" ]
