FROM ubuntu:20.04
MAINTAINER iskoldt
RUN apt update \
    && apt -y install python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /savebot
WORKDIR /savebot
RUN pip3 install --no-cache-dir -r requirements.txt
ENV MY_TOKEN empty
ENV MY_API_ID empty
ENV MY_API_HASH empty
ENV TARGET_CHAT_ID empty
CMD ["python3", "savebot.py"]
