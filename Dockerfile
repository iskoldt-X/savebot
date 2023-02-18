FROM ubuntu:20.04
MAINTAINER iskoldt
RUN apt update \
	&& apt -y install python3-pip git \
	&& pip3 install requests \
	&& pip3 install telebot \
	&& git clone https://github.com/iskoldt-X/savebot.git \
	&& cd /savebot \
	&& chmod +x savebot.py
WORKDIR /savebot
ENV TARGET_CHAT_ID empty
ENV MY_TOKEN empty
ENV MY_API empty
CMD ./savebot.py
