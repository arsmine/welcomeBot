#!/usr/bin/python3

# 30/07/18
# welcomeBot's purpose is welcoming the new users on the group
# and sending message(Every8HourMsg) to groups every 8 hours.

import logging
import telegram

from telegram import TelegramError, ParseMode, Update
from telegram.ext import  Updater, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

# give the bot's telegram name
BOTNAME='<botName>'

# telegram bot token
# https://core.telegram.org/bots
BOTTOKEN = '<telegram-bot-token>'

# the message that sends every 8 hours
# (to send custom messages, edit this)
Message = ("*Sample Message*")

# the message send interval in seconds
MessageInterval = 28800

# set up logging
root = logging.getLogger()
root.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

@run_async
def send_async(bot, *args, **kwargs):
	bot.sendMessage(*args, **kwargs)

def welcome(bot, update):
	global chat_id

	new_members = update.message.new_chat_members

	for member in new_members:
		first_name = member.first_name
		logging.info(str(member.first_name))

	message = update.message
	chat_id = message.chat.id
	logger.info('%s joined to chat %d (%s)',
	            first_name,
	            chat_id,
	            message.chat.title)

	# the message to send when a new user
	# enters the group.
	# (to send custome messages, edit this)
	text = str('$title\'a hoşgeldiniz.\n' +
	           '$username' + ', botlarımızı kullanmak için @arsminebot.\n' +
	           'Bol kazançlar dileriz.')
	text = text.replace('$username',
	                    first_name)\
	                    .replace('$title', message.chat.title)

	send_async(bot, chat_id=chat_id, text=text)

def empty_message(bot, update):
	new_members = update.message.new_chat_members
	for member in new_members:
		logging.info(str(member.first_name))
		first_name = member.first_name

		if first_name is not None:
			if first_name == BOTNAME:
				pass
			else:
				return welcome(bot, update)

def error(bot, update, error, **kwargs):
    """ Error handling """
    try:
        if isinstance(error, TelegramError)\
                and error.message == "Unauthorized"\
                or "PEER_ID_INVALID" in error.message\
                and isinstance(update, Update):

            logger.info('Removed chat_id %s from chat list'
                        % update.message.chat_id)
        else:
            logger.error("An error (%s) occurred: %s"
                         % (type(error), error.message))
    except:
        pass

def sendBotMessage(bot, job):
	global chat_id

	text=str(Every8HourMsg)

	bot.send_message(chat_id=chat_id,
	                 text=text,
	                 parse_mode=telegram.ParseMode.MARKDOWN)
	return

def main():
	updater = Updater(BOTTOKEN)

	job = updater.job_queue
	job_repeating = job.run_repeating(sendBotMessage, MessageInterval=28800, first=300)

	dp = updater.dispatcher
	dp.add_handler(MessageHandler([Filters.status_update], empty_message))
	dp.add_error_handler(error)

	update_queue = updater.start_polling(timeout=30)
	updater.idle()

if __name__ == '__main__':
	main()
