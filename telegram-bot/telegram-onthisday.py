#!/usr/bin/env python3
"""Telegram bot for onthisday.

Build it with: docker build -t telegram-onthisday .
Run it with something like: docker run -ti --rm -e EVENTS_TOKEN=your-telegram-token telegram-onthisday

Copyright 2019-2021 Davide Alberani <da@erlug.linux.it> Apache 2.0 license
"""

import os
import sys
import time
import logging
import subprocess
from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def getEvents(day=None):
    cmd = ['python3', '/onthisday/onthisday.py']
    if day:
        try:
            time.strptime(day, '%m/%d')
            cmd += ['--date', day]
        except Exception:
            pass
    if len(sys.argv) > 1:
        cmd += sys.argv[1:]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    try:
        stdout = stdout.strip()
        stdout = stdout.decode('utf8')
    except:
        return 'uh-oh: something was wrong with the encoding of the events; try again'
    if process.returncode != 0:
        return 'something terrible is happening: exit code: %s, stderr: %s' % (
                process.returncode, stderr.decode('utf8'))
    if not stdout:
        return 'sadness: the events list is empty; try again'
    return stdout


def events(bot, update):
    day = None
    txts = bot.message.text.split()
    if len(txts) == 2:
        day = txts[1]
    events = getEvents(day)
    logging.info('%s wants some news; serving:\n%s' % (bot.effective_user.username, events))
    bot.message.reply_text(events)


def about(bot, update):
    logging.info('%s required more info' % bot.effective_user.username)
    bot.message.reply_text('See https://github.com/alberanid/onthisday\n\n/today to use the current date\n\n/date 07/30 for July 30')


if __name__ == '__main__':
    if 'EVENTS_TOKEN' not in os.environ:
        print("Please specify the Telegram token in the EVENTS_TOKEN environment variable")
    logging.info('start serving very important facts')
    updater = Updater(os.environ['EVENTS_TOKEN'])
    updater.dispatcher.add_handler(CommandHandler('today', events, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('start', events, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('date', events, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('about', about))
    updater.dispatcher.add_handler(CommandHandler('help', about))
    updater.start_polling()
    updater.idle()
