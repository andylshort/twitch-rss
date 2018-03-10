"""
Twitch Active Streamer Script
"""

import os
import string
import random
import logging
import time
import datetime
import tzlocal
import pytz

import configparser
import requests
import os.path

import feedparser
from feedgen.feed import FeedGenerator

from flask import Flask

app = Flask(__name__)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read("auth.cfg")


minute = 60
delay = 5 * minute

headers = {
    "Accept": "application/vnd.twitchtv.v5+json",
    "Client-ID": config.get("OAuth", "clientID"),
    "Authorization": config.get("OAuth", "oauth_token")
}

out_file = "static/rss.xml"



if __name__ == "__main__":
    logger.debug("Obtaining active streamers")
    request = requests.get("https://api.twitch.tv/kraken/streams/followed", headers=headers)
    logger.debug("Returned " + str(request.status_code))

    # Successful response
    if request.status_code == 200:
        resp = request.json()

        os.makedirs(os.path.dirname(out_file), exist_ok=True)

        feedgen = FeedGenerator()
        feedgen.title("Twitch")
        feedgen.description("test rss feed")
        feedgen.link(href='http://localhost', rel='alternate' )


        for i in range(0, resp["_total"]):
            # Obtain stream information
            stream = resp["streams"][i]
            channel = stream["channel"]
            channel_name = channel["display_name"]
            game = channel["game"]
            status = channel["status"]
            url = channel["url"]

            # GLue info together
            title = channel_name + " is now streaming"
            description = "Playing {}<br/>\"{}\"".format(game, status)

            date = datetime.datetime.strptime(stream["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            date = date.replace(tzinfo=pytz.utc)
            date = date.astimezone(tz=tzlocal.get_localzone())

            # Create entry
            fe = feedgen.add_entry()
            fe.title(title)
            fe.description(description=description)
            fe.link(href=url, rel="alternate")
            fe.published(date)

        feedgen.rss_file(out_file, pretty=True)
