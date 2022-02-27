from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async
import requests
import re,os
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.ext.filters import Filters

API_KEY = os.environ.get('API_KEY')

def start(update: Update, context: CallbackContext):
    	update.message.reply_text(
		"Hello sir, Welcome to the Bot.Please write\
		/help to see the commands available.")
def help(update: Update, context: CallbackContext):
    	update.message.reply_text("""Available Commands :-
	    /bop - to fetch a random dog image""")
     
def unknown(update: Update, context: CallbackContext):
    	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

run_async
def bop(update, context):
    url = get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('bop',bop))
    # Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) 
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
    updater.start_webhook(listen="0.0.0.0",port=os.environ.get("PORT",443),
                          url_path=API_KEY,
                          webhook_url="https://bopdog.herokuapp.com/"+API_KEY)
    updater.idle()
    
if __name__ == '__main__':
    main()
    
    