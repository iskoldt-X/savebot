import requests
import telebot
import datetime

TARGET_CHAT_ID = myid
bot = telebot.TeleBot(mytoken)

@bot.message_handler(func=lambda message: message.chat.id == TARGET_CHAT_ID, content_types=['text', 'photo', 'audio', 'document', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact', 'poll', 'dice'])
def echo_all(message):
    bot.reply_to(message, 'copy.')
    print(message.chat.id, datetime.datetime.fromtimestamp(message.date).strftime("%Y-%m-%d-%H.%M.%S"), message.text)
    print(message)

    if message.photo:
        # If the message contains a photo, download it
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('photo.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
            
        afile = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(mytoken, file_info.file_path))
        file_extension = '.' + file_info.file_path.split('.')[-1]
        with open('afile' + file_extension, 'wb') as f:
            f.write(afile.content)
        
    if message.video:
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

bot.infinity_polling()
