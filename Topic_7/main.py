import telebot
import requests
import json

API_TOKEN = 'тут токена нет'
bot = telebot.TeleBot(API_TOKEN)

def translate(text):
    # Using MyMemoryTranslation API as an alternative to LibreTranslate
    url = "https://api.mymemory.translated.net/get"
    
    params = {
        'q': text,
        'langpair': 'ru|en'
    }    
    
    try:
        response = requests.get(url, params=params)
        translation = response.json()
        return translation['responseData']['translatedText']
    except Exception as e:
        print(f"Translation error: {e}")
        return "Translation service unavailable"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi, I'm a translation bot. Say something and I'll translate it!\
""")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """\
Type anything you want, and I'll translate it!\
""")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, translate(message.text))

def handler(event, context):
    message = telebot.types.Update.de_json(event['body'])
    bot.process_new_updates([message])
    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }