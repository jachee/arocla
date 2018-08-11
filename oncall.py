#! /usr/bin/env python

"""
Autmated On Call Rotation List App

Mostly a library of funcitons to be called by the Flask app.

Will also spit output to the commandline if run that way.
"""

import sys, os, datetime, fnmatch
import simplejson as json

mypath = os.path.abspath(os.path.dirname(__file__))
teamfile = os.path.join(mypath, 'teams.json')

today = datetime.datetime.now() # Got the current time
# today = datetime.datetime(2017, 9, 9, 15, 0, 20, 912320) # Fuuuuuture!

this_week = int(today.strftime('%U')) # Converted to a numeric week number
this_month = int(today.strftime('%-m'))
this_day = int(today.strftime('%-j'))

def load_teams():
    try:
        source = open(teamfile)
    except IOError:
        sys.exit("No %s file found! Exiting." % teamfile)
    except:
        sys.exit("Error opening %s for reading. Exiting." % teamfile)

    try:
        teams = json.load(source)
    except:
        sys.exit("Error while reading team info from %s" % teamfile)

    return teams


def rotate_list(target_list, offset):
    """
    Takes a list and an integer and cycles the items in the list by
    the offset defined by the integer, wrapping as necessary.
    """
    offset = offset % len(target_list)
    return target_list[offset:] + target_list[:offset]


def load_list(team):
    """
    Takes a team as a dict that's a team Description and a  JSON file
    for that team. Returns a tuple of the team name and the contents of the
    JSON file as a list of dicts
    """
    try:
        source = open(os.path.join(mypath, '%s' % team['filename']))
    except IOError:
        sys.exit("No %s.json file found! Exiting." % team['filename'])
    except:
        sys.exit("Error opening %s.json for reading. Exiting." % team['filename'])

    try:
        members = json.load(source)
    except:
        sys.exit("Error loading %s. Does it exist?" % team['filename'])

    return (team['teamname'], members)

def output_list(teamlist, team):
    """
    Takes a list of dictionaries and the other is a string.
    """
    desc = team['teamname']
    print("%s Team List:" % desc)
    print(teamlist)


def whos_up(teamlist, interval='week', freq=1):
    """
    Takes a tuple as from load_list() and an optional string and integer,
    returns a tuple of the team name and rotated list of dictionaries.
    """
    # print(teaminfo)
    if interval == "month":
        cycle = int(this_month / freq)
    elif interval == "day":
        cycle = int(this_day / freq)
    else:
        cycle = int(this_week / freq) # What cycle number are we on?

    desc = teamlist[0]
    members = teamlist[1]
    if __name__ == '__main__':
        print("%s Current on-call :" % desc)
        print(rotate_list(members, cycle)[0])

    return (desc, rotate_list(members, cycle))

def main():
    print("mypath: %s" % mypath)
    teams = load_teams()
    for team in teams:
        teamlist = (load_list(team))
        interval = team['interval']
        freq = team['freq']
        whos_up(teamlist, interval, freq)
        output_list(teamlist, team)


    print("Done!")


if __name__ == '__main__':
    main()
