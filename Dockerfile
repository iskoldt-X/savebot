FROM python:3.9-slim-buster AS builder
RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt .
RUN pip3 install --no-cache-dir --user -r requirements.txt
FROM python:3.9-slim-buster
MAINTAINER iskoldt
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . /savebot
WORKDIR /savebot
ENV MY_TOKEN empty
ENV MY_API_ID empty
ENV MY_API_HASH empty
ENV TARGET_CHAT_ID empty
CMD ["python3", "savebot.py"]
