import atexit

import subprocess

from flask import Flask, current_app

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)


@app.route("/")
def index():
    return "Twitch RSS Feed"

@app.route("/rss")
def rss():
    return current_app.send_static_file("rss.xml")

def update_rss_feed():
    print("Updating RSS feed...")
    subprocess.call(["python", "twitch_feed.py"])

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=update_rss_feed,
    trigger=IntervalTrigger(minutes=5),
    id='update_rss_feed',
    name='Updates the RSS feed of live, followed streams',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

update_rss_feed()
app.run(host="0.0.0.0", debug=True)