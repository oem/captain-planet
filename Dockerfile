FROM python:3.8-slim-buster
ADD . /
WORKDIR /
RUN pip install -r ./requirements.txt
