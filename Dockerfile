FROM python:3.11.0-slim

RUN set -eux; useradd wormhole -d /server;
RUN apt-get update -y
RUN apt-get install -y wget libgl1 libglib2.0-0 libturbojpeg0

COPY . /server
WORKDIR /server

RUN pip3 install -r requirements.txt
RUN pip3 install PyTurboJPEG

RUN wget https://upload.wikimedia.org/wikipedia/commons/transcoded/a/a5/Spring_-_Blender_Open_Movie.webm/Spring_-_Blender_Open_Movie.webm.1080p.webm -O /server/video.webm

USER wormhole:wormhole

CMD [ "python3", "main.py"]
