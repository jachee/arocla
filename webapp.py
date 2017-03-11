#! /usr/local/env python
"""
webapp.py - flaskify the oncall app.
"""

from oncall import whos_up, rotate_list, load_list
from flask import *
import datetime

app = Flask(__name__)

groups = ("system", "network", "mobility") # Each of these should have a <type>admins.json file
today = datetime.datetime.now() # Got the current time
#today = datetime.datetime(2017, 2, 6, 9, 0, 20, 912320) # Fuuuuuture!

week = int(today.strftime('%U')) # Converted to a numeric week number
weeks_per_cycle = 2  # Edit this to control how long each person is on-call.
cycle = int(week / weeks_per_cycle) # What cycle number are we on?

if week % weeks_per_cycle == 0:         # Zero modulus is a fresh cycle
    if int(today.strftime('%w')) < 2:   # If Sunday or Monday on a fresh cycle:
        cycle = cycle - 1               # Back up to last person who's on call
        if int(today.strftime('%w')) == 1 and int(today.strftime('%-H')) >= 8:
            cycle = cycle + 1           # Unless it's after 0800 on Monday


def list_loop():
    big_list = []
    for kind in groups:
        admins = (load_list(kind), kind)
        big_list.append((rotate_list(admins[0], cycle), kind))
    # print "Full Admins List:"
    # print big_list
    return big_list


@app.route("/")
def index():
    admins = list_loop()
    return render_template('oncall.html', groups = admins)


def main():
    app.debug = True                   # Set this to False for production
    app.run(host="0.0.0.0", port=5002) # Set this to bind to the correct socket

if __name__ == '__main__':
    main()
