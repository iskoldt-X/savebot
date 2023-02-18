#!/usr/bin/python3
import requests
import telebot
import datetime
import os
import sys

TARGET_CHAT_ID = os.environ.get("TARGET_CHAT_ID")
MY_TOKEN = os.environ.get("MY_TOKEN")
MY_API = os.environ.get("MY_API")

if TARGET_CHAT_ID != 'empty':
    TARGET_CHAT_ID = int(TARGET_CHAT_ID)

if TARGET_CHAT_ID == 'empty' and MY_TOKEN != 'empty':
    #just give me the chat id.
    bot = telebot.TeleBot(MY_TOKEN)
    def just_chat_id(message):
        timerr = datetime.datetime.fromtimestamp(message.date).strftime("%Y-%m-%d-%H.%M.%S")
        thechatid = message.chat.id
        bot.reply_to(message, 'Your CHAT_ID is: ' + str(thechatid))
        print(thechatid, timerr)
        sys.exit(0)
    bot.infinity_polling()

parent_dir = 'messages'

all_content = ['text', 'photo',
               'audio', 'document',
               'sticker', 'video',
               'video_note', 'voice',
               'location', 'contact',
               'poll', 'dice']

def create_fld(folder_name):
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

create_fld(parent_dir)
for thefolder in all_content:
    create_fld(parent_dir + '/' + thefolder)

bot = telebot.TeleBot(MY_TOKEN)
@bot.message_handler(func=lambda message: message.chat.id == TARGET_CHAT_ID, content_types=all_content)

def echo_all(message):
    timerr = datetime.datetime.fromtimestamp(message.date).strftime("%Y-%m-%d-%H.%M.%S")
    thechatid = message.chat.id
    messageid = message.message_id
    filenamehead = str(messageid) + '.' + timerr
    content_type = message.content_type
    myfilepath = ''
    moreinfo = ''
    
    #message forward or not
    if message.forward_from_chat:
        someinfo = str(message.forward_from_chat)
        if message.forward_from_message_id:
            someinfo = someinfo + '\n' + str(message.forward_from_message_id)
    elif message.forward_from:
        someinfo = str(message.forward_from)
    else:
        someinfo = ''
    
    print(thechatid, timerr, content_type)
    print(message)
    
    if message.text:
        messagetext = message.text
        with open(parent_dir + '/text/' + filenamehead + '-' + messagetext[:20] + '.txt', 'w') as f:
            f.write(messagetext + '\n')
    else:
        if content_type in all_content:
            content = getattr(message, content_type)
            if content:
                print(content, type(content))
                if isinstance(content, telebot.types.Audio):
                    file_id = content.file_id
                elif isinstance(content, telebot.types.VideoNote):
                    file_id = content.thumb.file_id
                else:
                    file_id = content[-1].file_id
                file_info = bot.get_file(file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                extension = ''
                if content_type == 'photo':
                    extension = '.jpg'
                elif content_type == 'video':
                    extension = '.mp4'
                elif content_type == 'document':
                    if message.document.file_name:
                        extension = message.document.file_name
                
                #message have caption or not
                if message.caption:
                    moreinfo = message.caption
                    someinfo = filenamehead + '\n' + someinfo + '\n' + moreinfo + '\n' + myfilepath + '\n'
                else:
                    someinfo = filenamehead + '\n' + someinfo + '\n' + myfilepath + '\n'

                if moreinfo != '':
                    moreinfo = '-' + moreinfo[:20]
                myfilepath = parent_dir + '/' + content_type + '/' + filenamehead + moreinfo + extension

                #save the file
                with open(myfilepath, 'wb') as new_file:
                    new_file.write(downloaded_file)

                #creata a text file to record the existing of the non-text file
                with open(parent_dir + '/text/' + filenamehead + '.' + content_type + moreinfo + '.txt', 'w') as f:
                    f.write(someinfo)

        else:
            print('not supported yet')
            bot.reply_to(message, 'not supported yet')
             
    bot.reply_to(message, 'Roger that.')
    
bot.infinity_polling()
