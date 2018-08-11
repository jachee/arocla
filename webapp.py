#! /usr/local/env python
"""
This does the actual web-serving for the Automated On-Call List
            Rotation app.
"""

import oncall
from flask import *
# import datetime, fnmatch, os

app = Flask(__name__)
# mypath = os.path.abspath(os.path.dirname(__file__))

# teams = ["system", "network", "mobility"] # Each of these should have a <type>admins.json file
# today = datetime.datetime.now() # Got the current time
#today = datetime.datetime(2017, 2, 6, 9, 0, 20, 912320) # Fuuuuuture!

# week = int(today.strftime('%U')) # Converted to a numeric week number
# weeks_per_cycle = 2  # Edit this to control how long each person is on-call.
# cycle = int(week / weeks_per_cycle) # What cycle number are we on?

# if week % weeks_per_cycle == 0:         # Zero modulus is a fresh cycle
#     if int(today.strftime('%w')) < 2:   # If Sunday or Monday on a fresh cycle:
#         cycle = cycle - 1               # Back up to last person who's on call
#         if int(today.strftime('%w')) == 1 and int(today.strftime('%-H')) >= 8:
#             cycle = cycle + 1           # Unless it's after 0800 on Monday


def list_loop():
    teamslist = []
    teams = oncall.load_teams()
    for team in teams:
        interval = team['interval']
        freq = team['freq']
        teaminfo = (oncall.load_list(team))
        teamslist.append(oncall.whos_up(teaminfo, interval, freq))
    return teamslist


@app.route("/")
def index():
    rotatedteams = list_loop()
    return render_template('results.html', teams = rotatedteams)


def main():
    app.debug = True                   # Set this to False for production
    app.run(host="0.0.0.0", port=5002) # Set this to bind to the correct socket

if __name__ == '__main__':
    main()
