**English** | [中文](https://icecoland.com/2023/02/19/savebot/)

# Savebot
Text, photos, videos... Save everything you throw to the telegram bot!

<img src="https://img.shields.io/github/license/iskoldt-X/savebot.svg"/> <img src="https://img.shields.io/docker/pulls/iskoldt/savebot.svg"/>

## Features

* Supported platforms: `amd64`, `arm64`.
* Save text messages into txt files with message id and the time as label.
* Save Photos and Videos into corresponding folders, and the caption into txt files.
* Nailed files larger than 20MB by using [MTProto API](https://docs.pyrogram.org/topics/mtproto-vs-botapi#advantages-of-the-mtproto-api).


## Requirements

We need at least a telegram Bot and a Python3 environment to run this project.

Don't worry, you can easily get a telegram bot from [@BotFather](https://core.telegram.org/bots#how-do-i-create-a-bot).

Python3 environment is not a big deal. If you can use Docker, you are basicly a savebot master!


## Run savebot in Docker

If you got your `BOT_TOKEN`, your can use savebot to get your `TARGET_CHAT_ID`:

```
docker run -d \
  --rm \
  --name savebot \
  -e MY_TOKEN=<BOT_TOKEN> \
  iskoldt/savebot:latest
```
Then send anything to your bot, you will get your `TARGET_CHAT_ID`

Run this:
```
docker run -d \
  --name savebot \
  --restart unless-stopped \
  -e MY_TOKEN=<BOT_TOKEN> \
  -e TARGET_CHAT_ID=<TARGET_CHAT_ID> \
  -v <yourdir>:/savebot/messages \
  iskoldt/savebot:latest
```

Telegram bot API is limited on file size, so we need [MTProto API](https://docs.pyrogram.org/topics/mtproto-vs-botapi#advantages-of-the-mtproto-api), get it here [Obtaining api_id](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id)

Now you have `API_ID` and `API_HASH`, congrats!🎉

You can use savebot to save any file!

```
docker run -d \
  --name savebot \
  --restart unless-stopped \
  -e MY_API_ID=<API_ID> \
  -e MY_API_HASH=<API_HASH> \
  -e MY_TOKEN=<BOT_TOKEN> \
  -e TARGET_CHAT_ID=<TARGET_CHAT_ID> \
  -v <yourdir>:/savebot/messages \
  iskoldt/savebot:latest
```


## Run savebot in Python3 environment

Download savebot from github and Get your `TARGET_CHAT_ID`:

```
git clone https://github.com/iskoldt-X/savebot.git
cd savebot
pip3 install -r requirements.txt

#keep the word empty if you don't have it
export TARGET_CHAT_ID=empty
export MY_TOKEN=<BOT_TOKEN>
export MY_API_ID=empty
export MY_API_HASH=empty

python3 savebot.py
```

Then send anything to your bot, you will get your `TARGET_CHAT_ID`

```
export TARGET_CHAT_ID=<your TARGET_CHAT_ID>
python3 savebot.py
```

## Acknowledgments

We are grateful to Telethon and Pyrogram for providing such great APIs that enable us to create telegram bots like this one.

## Statement

Savebot is just a tool for locally saving your Telegram content. If you decide to save the content to public cloud storage, please make sure that you comply with the relevant laws and regulations on privacy and data protection.

## License

This project is licensed under the terms of the MIT license.
