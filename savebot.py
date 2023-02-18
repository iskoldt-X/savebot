#!/usr/bin/python3
import requests
import telebot
import datetime
import os


TARGET_CHAT_ID = int(os.environ.get("TARGET_CHAT_ID"))
MY_TOKEN = os.environ.get("MY_TOKEN")


all_content = ['text', 'photo', 'audio', 'document', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact', 'poll', 'dice']

        
for thefolder in all_content:
    if not os.path.isdir(thefolder):
        os.makedirs(thefolder)
        print(thefolder, " do not exist! created it.")


bot = telebot.TeleBot(MY_TOKEN)
@bot.message_handler(func=lambda message: message.chat.id == TARGET_CHAT_ID, content_types=all_content)

def echo_all(message):
    
    timerr = datetime.datetime.fromtimestamp(message.date).strftime("%Y-%m-%d-%H.%M.%S")
    thechatid = message.chat.id
    messageid = message.message_id
    filenamehead = str(messageid) + '.' + timerr
    content_type = message.content_type
    myfilepath = ''
    
    
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
        with open('text/' + filenamehead + '.txt', 'w') as f:
            f.write(messagetext + '\n')
    else:
        if content_type in all_content:
            print('yess')
            content = getattr(message, content_type)
            if content:
                known_type = True
                print(content, type(content))
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
                
                myfilepath = content_type + '/' + filenamehead + extension
                with open(myfilepath, 'wb') as new_file:
                    new_file.write(downloaded_file)
           
        else:
            print('not supported yet')
            bot.reply_to(message, 'not supported yet')
        
        if message.caption:
            someinfo = filenamehead + '\n' + someinfo + '\n' + message.caption + '\n' + myfilepath + '\n'
        else:
            someinfo = filenamehead + '\n' + someinfo + '\n' + myfilepath + '\n'
            
        with open('text/' + filenamehead + '.txt', 'w') as f:
            f.write(someinfo)
        
         
            
    bot.reply_to(message, 'Roger that.')
    
bot.infinity_polling()
