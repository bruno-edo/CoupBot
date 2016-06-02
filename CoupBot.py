""""
    Ownership:
                Bruno Eduardo D'Angelo - Brazil, 2016

    Contributors:
                Rian Provesano Reis

"""


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging


#Coup Bot classes imports
import Commands as c


# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)




def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("226711778:AAGWaWA7fgvq6tXjvH5SxwK3FsJsHmGt_MM")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", c.startGame))
    dp.add_handler(CommandHandler("stop", c.stop))
    dp.add_handler(CommandHandler("creategame", c.createGame))
    dp.add_handler(CommandHandler("join", c.joinGame))
    dp.add_handler(CommandHandler("game", c.getGame))
    dp.add_handler(CommandHandler("hello", c.hello))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], c.checkPlays))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()