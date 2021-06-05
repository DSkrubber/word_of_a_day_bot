"""
Simple Bot for Telegram to translate english<->russian words and study english language.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Possibilities: send word of a day , set daily timer for sending word of a day in chat,
translate words from english to russian and vice versa.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


import logging
import time
import datetime
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from wod_parser import request_wod, request_trans


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def set_timer(update: Update, context: CallbackContext):
    """
    Sets daily timer for bot to send 'word of a day' message in present chat if calling for the first time
    or resets existing timer to user defined value.
    Defines format for user's message with time and then gets time from message if format is correct,
    otherwise aborts and sends caution.
    If user doesn't define time sets timer to default 12:00 (UTC + 3).
    """
    chat_id = update.message.chat_id    # To send only in particular chat.
    divisors = ' :'
    time_set = (update.message.text[35:] if '@simple_word_of_a_day_bot' in update.message.text else
                update.message.text[10:])
    for div in divisors:
        if div in time_set:
            try:
                hours, minutes = time_set.split(div)
                break
            except:
                update.effective_chat.send_message('Incorrect time format. Use only "hh:mm" or "hh mm".')
                return
        else:
            try:
                hours, minutes = time_set[:2], time_set[2:5]
            except:
                update.effective_chat.send_message('Incorrect time format. Use only "hh:mm" or "hh mm".')
                return
    if not time_set:
        hours, minutes = '12', '00'
    try:
        context.job_queue.scheduler.remove_all_jobs()    # Delete all previous schedullers if exist.
        context.job_queue.run_daily(
            wordofday_timer, datetime.time(int(hours)-3, int(minutes), 0), context=chat_id, name=str(chat_id)
        )
    except:
        update.effective_chat.send_message('Incorrect time format. Use only "hh:mm" or "hh mm".')
        return
    update.effective_chat.send_message('Timer is set and updated!\n'
                                       'Exactly at %s:%s (UTC +3) I will send you the word of a day!'
                                       % (hours, minutes))


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def wordofday_timer(context: CallbackContext) -> None:
    '''
    This function is used for sending result of 'request_wod' function from 'wod_parser' module
    (which returns 'word of a day') if called via settimer function.
    Also sends default sticker from 'Witcher' sticker-pack from Telegram.
    Uses 'context', doesn't use 'update' arguments.
    '''
    job = context.job
    word, definition = request_wod()
    context.bot.send_message(job.context, text='And the word of the day is...')
    time.sleep(1)
    context.bot.send_message(job.context, text=word.upper())
    time.sleep(1)
    context.bot.send_message(job.context, text='And that means...[looking in dictionary]')
    time.sleep(2)
    context.bot.send_message(job.context, text='Ah!\n' + definition.capitalize())
    time.sleep(1)
    context.bot.send_sticker(job.context,
                             sticker='CAACAgIAAxkBAAECX4ZguPYva-R9gXn3DQ86nx3L8INttAACQwEAAorsmwgeLLIwn1VwWB8E')


def wordofday(update: Update, _: CallbackContext) -> None:
    '''
    This function is used for sending result of 'request_wod' function from 'wod_parser' module
    (which returns 'word of a day') if called via 'wordofday' command in Telegram (without settimer).
    Also sends default sticker from 'Witcher' sticker-pack from Telegram.
    '''
    word, definition = request_wod()
    update.effective_chat.send_message('And the word of the day is...')
    time.sleep(1)
    update.effective_chat.send_message(word.upper())
    time.sleep(1)
    update.effective_chat.send_message('And that means...[looking in dictionary]')
    time.sleep(2)
    update.effective_chat.send_message('Ah!\n' + definition.capitalize())
    time.sleep(1)
    update.effective_chat.send_sticker(
        sticker='CAACAgIAAxkBAAECX4ZguPYva-R9gXn3DQ86nx3L8INttAACQwEAAorsmwgeLLIwn1VwWB8E'
    )


def translate(update: Update, _: CallbackContext) -> None:
    '''
    This function is used for sending result of 'request_trans' function from 'wod_parser' module
    (which returns translation for user defined word with Telegram command 'translate').
    Also sends default sticker from 'Witcher' sticker-pack from Telegram.
    '''
    users_word = (update.message.text[11:] if '@simple_word_of_a_day_bot' not in update.message.text else
                  update.message.text[36:])
    translation = request_trans(users_word)
    if len(translation) < 300:
        update.effective_chat.send_message("Hmm...let's see [looking in dictionary]")
        time.sleep(2)
        update.effective_chat.send_message('So...\n%s %s' % (users_word, translation))
        time.sleep(1)
        update.effective_chat.send_sticker(
            sticker='CAACAgIAAxkBAAECX4ZguPYva-R9gXn3DQ86nx3L8INttAACQwEAAorsmwgeLLIwn1VwWB8E'
        )
    else:
        update.effective_chat.send_message('error')


# Use for testing bot.
# def echo(update: Update, _: CallbackContext) -> None:
#     """Echo the user message."""
#     pass


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1805457445:AAHHL9itZY935yva4Ir7rYOVzVO-BUinWSI")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("wordofday", wordofday))
    dispatcher.add_handler(CommandHandler("settimer", set_timer))
    dispatcher.add_handler(CommandHandler("translate", translate))

    # Use for testing.
    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()