FROM python:3.9-slim-buster
MAINTAINER iskoldt
RUN apt-get update && apt-get install -y build-essential && apt-get clean
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /savebot
WORKDIR /savebot
ENV MY_TOKEN empty
ENV MY_API_ID empty
ENV MY_API_HASH empty
ENV TARGET_CHAT_ID empty
CMD ["python3", "savebot.py"]
