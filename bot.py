#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import Updater, ReplyKeyboardMarkup, ParseMode
from telegram.utils.botan import Botan
import logging
import pyUniVeronaBot
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('settings.ini')
token = str(config.get('main', 'token'))
botan_token = str(config.get('main', 'botan'))
b = Botan(botan_token)

TOPCOMMANDS = ['start', 'home', 'help', 'botinfo',
               'mensa', 'aulastudio', 'biblioteca']

commands = pyUniVeronaBot.commandList()

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def home(bot, update):
    pyUniVeronaBot.writedb(update.message.to_dict())
    reply, markup = pyUniVeronaBot.home()
    b.track(update.message, update.message.text)
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))


def botinfo(bot, update):
    pyUniVeronaBot.writedb(update.message.to_dict())
    reply, markup = pyUniVeronaBot.botInfo()
    b.track(update.message, update.message.text)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=reply,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=ReplyKeyboardMarkup(markup))


def mensa(bot, update):
    pyUniVeronaBot.writedb(update.message.to_dict())
    reply, markup = pyUniVeronaBot.mensa()
    b.track(update.message, update.message.text)
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))


def aulastudio(bot, update):
    pyUniVeronaBot.writedb(update.message.to_dict())
    reply, markup = pyUniVeronaBot.aulastudio()
    b.track(update.message, update.message.text)
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))


def biblioteca(bot, update):
    pyUniVeronaBot.writedb(update.message.to_dict())
    reply, markup = pyUniVeronaBot.biblioteca()
    b.track(update.message, update.message.text)
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))


def replier(bot, update):
    pyUniVeronaBot.writedb(update.message.to_dict())
    b.track(update.message, update.message.text)
    command = str(update.message.text).replace('/', '')
    command.lower()
    reply, markup, lat, lon = pyUniVeronaBot.replier(command)
    bot.sendMessage(update.message.chat_id,
                    text=reply,
                    reply_markup=ReplyKeyboardMarkup(markup))
    if lat is not None and lon is not None:
        bot.sendLocation(update.message.chat_id,
                         latitude=lat,
                         longitude=lon)


def position(bot, update):
    msg = update.message.to_dict()
    pyUniVeronaBot.writedb(msg)
    b.track(update.message, 'position')
    try:
        usrCoord = msg['location']
        reply, markup = pyUniVeronaBot.position(usrCoord)
        bot.sendMessage(update.message.chat_id,
                        text=reply,
                        reply_markup=ReplyKeyboardMarkup(markup))
    except:
        pass


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("help", home)
    dp.addTelegramCommandHandler("start", home)
    dp.addTelegramCommandHandler("home", home)

    dp.addTelegramCommandHandler("botinfo", botinfo)

    dp.addTelegramCommandHandler("mensa", mensa)
    dp.addTelegramCommandHandler("aulastudio", aulastudio)
    dp.addTelegramCommandHandler("biblioteca", biblioteca)

    for command in commands:
        dp.addTelegramCommandHandler(command, replier)

    dp.addTelegramMessageHandler(position)

    dp.addErrorHandler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
