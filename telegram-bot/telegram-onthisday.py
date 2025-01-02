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
from telegram import Update
from telegram.ext import Application, CommandHandler

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
    except Exception:
        return 'uh-oh: something was wrong with the encoding of the events; try again'
    if process.returncode != 0:
        return 'something terrible is happening: exit code: %s, stderr: %s' % (
                process.returncode, stderr.decode('utf8'))
    if not stdout:
        return 'sadness: the events list is empty; try again'
    return stdout


async def events(update, context):
    day = None
    txts = update.message.text.split()
    if len(txts) == 2:
        day = txts[1]
    events = getEvents(day)
    logging.info('%s wants some news; serving:\n%s' % (update.effective_user.username, events))
    await update.message.reply_text(events)


async def about(update, context):
    logging.info('%s required more info' % update.effective_user.username)
    await update.message.reply_text('See https://github.com/alberanid/onthisday\n\n/today to use the current date\n\n/date 07/30 for July 30')


if __name__ == '__main__':
    if 'EVENTS_TOKEN' not in os.environ:
        print("Please specify the Telegram token in the EVENTS_TOKEN environment variable")
    logging.info('start serving very important facts')
    application = Application.builder().token(os.environ['EVENTS_TOKEN']).build()

    application.add_handler(CommandHandler('today', events, has_args=False))
    application.add_handler(CommandHandler('start', events, has_args=False))
    application.add_handler(CommandHandler('date', events, has_args=True))
    application.add_handler(CommandHandler('about', about))
    application.add_handler(CommandHandler('help', about))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
