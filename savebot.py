#!/usr/bin/python3

# Import the required libraries
from pyrogram import Client
import datetime
import telebot
import os

def create_fld(folder_name):
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

#by default, we will only use
#telebot, Pyrogram requires
#more api than telebot.
pyrogram_flag = False

parent_dir = 'messages'
all_content = ['text', 'photo',
               'audio', 'document',
               'sticker', 'video',
               'video_note', 'voice',
               'location', 'contact',
               'poll', 'dice']

MY_TOKEN = os.environ.get("MY_TOKEN")
MY_API_ID = os.environ.get("MY_API_ID")
MY_API_HASH = os.environ.get("MY_API_HASH")
TARGET_CHAT_ID = os.environ.get("TARGET_CHAT_ID")

bot = telebot.TeleBot(MY_TOKEN)

#if the TARGET_CHAT_ID is empty,
# that means this run only needs
# to reply the chat id for the user
if TARGET_CHAT_ID != 'empty':
    TARGET_CHAT_ID = int(TARGET_CHAT_ID)
else:
    print('Oh no. Now I need to send you your Chat ID.')
    #just give me the chat id.
    @bot.message_handler(content_types=all_content)
    def just_chat_id(message):
        bot.reply_to(message, 'Your CHAT_ID is: ' + str(message.chat.id))
        bot.stop_polling()
        os._exit(0)
    bot.infinity_polling()

#if MY_API_ID is not 'empty',
#that means the user wants to
#use pyrogram as well
if MY_API_ID != 'empty':
    pyrogram_flag = True
    # Create a Pyrogram client
    client = Client('my_session', MY_API_ID, MY_API_HASH, bot_token=MY_TOKEN)

    # Define a function to download a file
    #download_file(123132131, 123)
    def download_file(chat_id, message_id, filepath_):
        # Use the Pyrogram client to download the file
        with client:
            message = client.get_messages(chat_id, message_id, filepath_)
            if message.document:
                message.download(file_name=message.document.file_name)
            else:
                message.download()

# Now we are talking!
# Just create those dirs
create_fld(parent_dir)
for thefolder in all_content:
    create_fld(parent_dir + '/' + thefolder)

# Our bot is here! let's go!
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
    #print(message)
    
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
                    file_size = content.file_size
                elif isinstance(content, telebot.types.VideoNote):
                    file_id = content.file_id
                    file_size = content.file_size
                elif isinstance(content, telebot.types.Video):
                    file_id = content.file_id
                    file_size = content.file_size
                else:
                    file_id = content[-1].file_id
                    file_size = content[-1].file_size
                print(file_size)

                if file_size < 20000000:
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
                if file_size < 20000000:
                    with open(myfilepath, 'wb') as new_file:
                        new_file.write(downloaded_file)
                else:
                    if pyrogram_flag:
                        download_file(TARGET_CHAT_ID, messageid, myfilepath)


                #creata a text file to record the existing of the non-text file
                with open(parent_dir + '/text/' + filenamehead + '.' + content_type + moreinfo + '.txt', 'w') as f:
                    f.write(someinfo)

        else:
            print('not supported yet')
            bot.reply_to(message, 'not supported yet')
             
    bot.reply_to(message, 'Roger that.')
    
bot.infinity_polling()
