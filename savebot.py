import requests
import telebot
import datetime
import os


TARGET_CHAT_ID = int(os.environ.get("TARGET_CHAT_ID"))
MY_TOKEN = os.environ.get("MY_TOKEN")

folderlist = ['messages']

for thefolder in folderlist:
    if not os.path.isdir(thefolder):
        os.makedirs(thefolder)
        print(thefolder, " do not exist! created it.")

bot = telebot.TeleBot(MY_TOKEN)
@bot.message_handler(func=lambda message: message.chat.id == TARGET_CHAT_ID, content_types=['text', 'photo', 'audio', 'document', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact', 'poll', 'dice'])

def echo_all(message):
    
    timerr = datetime.datetime.fromtimestamp(message.date).strftime("%Y-%m-%d-%H.%M.%S")
    thechatid = message.chat.id
    messageid = message.message_id
    filenamehead = str(messageid) + '.' + timerr + '.'
    
    
    print(thechatid, timerr, messagetext)
    print(message)
    
    if message.text:
        messagetext = message.text
        with open('messages/' + filenamehead + '.txt', 'w') as f:
            f.write(messagetext + '\n')
            
    elif message.photo:
        # If the message contains a photo, download it
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('photo.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
            
        afile = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(MY_TOKEN, file_info.file_path))
        file_extension = '.' + file_info.file_path.split('.')[-1]
        with open('afile' + file_extension, 'wb') as f:
            f.write(afile.content)
        
    elif message.video:
        # If the message contains a video, download it
        file_id = message.video.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('video.mp4', 'wb') as new_file:
            new_file.write(downloaded_file)

    if message.document:
        # If the message contains a document, download it
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(message.document.file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
            
    bot.reply_to(message, 'Roger that.')
    
bot.infinity_polling()
