#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Pablo Iranzo Gómez
# Description: Telegram User Client

import asyncio
import datetime
import logging
import re
import sys
import time
import urllib
import urllib.parse as urlparse
from string import Template
from urllib.parse import urlencode
from urllib.request import urlopen

import dateutil.parser
import pytz
import requests
from databases import Database
from dateutil.relativedelta import relativedelta
from telethon import TelegramClient, events, functions

# Connect to database
database = Database("sqlite:///fuzzy.db")

# Define headers for our 'browser'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
}

# Configure logging
# Enable for telethon debug
# logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("fuzzy")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s : %(name)s : %(funcName)s(%(lineno)d) : %(levelname)s : %(message)s"
)

# create console handler and set level to debug
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(console)

# create file logger
filename = "fuzzy.log"

file = logging.FileHandler(filename)
file.setLevel(logging.DEBUG)
file.setFormatter(formatter)
logger.addHandler(file)


async def getwords(type, gid=0):
    """
    Gets words from database according to criteria
    :param type: word classifier
    :param gid: group to match
    :return: array of words
    """

    if gid is not False:
        sql = 'SELECT word FROM wordlists WHERE gid="%s" AND type="%s"' % (gid, type)
    else:
        sql = 'SELECT word FROM wordlists WHERE type="%s"' % type

    # Process all entries in wordlist table
    words = []
    wordlist = await database.fetch_all(sql)
    for word in wordlist:
        words.append("%s" % word[0])

    return sorted(set(words))


def utize(date):
    """
    Converts date to UTC tz
    :param date: date to convert
    :return:
    """

    tz = pytz.timezone("GMT")

    try:
        code = date.astimezone(tz)

    except:
        try:
            code = date.replace(tzinfo=tz)
        except:
            code = date

    return code


async def config(key, default=False, gid=0):
    """
    Gets configuration from database for a given key
    :param gid: group ID to check
    :param key: key to get configuration for
    :param default: value to return for key if not define or False
    :return: value in database for that key
    """

    string = (
        key,
        gid,
    )
    sql = "SELECT key,value FROM config WHERE key='%s' AND id='%s';" % string
    value = await database.fetch_one(sql)

    try:
        # Get value from SQL query
        value = value[1]

    except:
        # Value didn't exist before, return default or False
        value = default

    return value


async def quitlooper(update):
    """
    Proceses incoming messages for /quit messages
    :param update: Update received
    """

    text = str(update.text)
    user = await update.get_sender()
    client = update.client

    if text == "/quit" and user.username == "iranzo":
        logger.debug("Exitting because of /quit command")
        await client.send_read_acknowledge(
            await update.get_input_chat(), clear_mentions=True
        )
        sys.exit(0)


# Main code
async def main():
    """
    Main code
    :return: none
    """

    # Open database connection
    await database.connect()

    # Telegram Client variables
    proxy = None
    session = "fuzzer"
    api_id = API_ID
    api_hash = API_HASH

    # Use the client in a `with` block. It calls `start/disconnect` automatically.
    while True:
        logger.debug("Starting execution loop")
        async with TelegramClient(session, api_id, api_hash, proxy=proxy) as client:
            # Check for loop quit commands
            client.add_event_handler(quitlooper, events.NewMessage())

            # Run the client until Ctrl+C is pressed, or the client disconnects
            print("(Press Ctrl+C to stop this)")

            # get missed messages while offline
            await client.catch_up()
            
            # YOURCODE for sending messages
            await client.send_message("CHAT,USER,ETC", "TEXT TO SEND")

            logger.debug("Run until disconnect")
            await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
