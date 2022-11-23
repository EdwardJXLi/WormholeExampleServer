FROM python:3.10.8-slim

RUN set -eux; useradd wormhole -d /server;
RUN apt-get update -y
RUN apt-get install -y wget libgl1 libglib2.0-0

COPY . /server
WORKDIR /server

RUN pip3 install -r requirements.txt

RUN wget https://upload.wikimedia.org/wikipedia/commons/a/a5/Spring_-_Blender_Open_Movie.webm -O /server/video.webm

USER wormhole:wormhole

CMD [ "python3", "main.py"]
