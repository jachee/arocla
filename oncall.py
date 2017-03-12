#! /usr/bin/env python

"""
On Call Rotator - Less-Goldbergian Edition.
"""

import sys, os, datetime, fnmatch
import simplejson as json

mypath = os.path.abspath(os.path.dirname(__file__))


today = datetime.datetime.now() # Got the current time
# today = datetime.datetime(2017, 9, 9, 15, 0, 20, 912320) # Fuuuuuture!

week = int(today.strftime('%U')) # Converted to a numeric week number
weeks_per_cycle = 2  # Edit this to control how long each person is on-call.
cycle = int(week / weeks_per_cycle) # What cycle number are we on?

teams = []
for file in os.listdir(mypath):
     if fnmatch.fnmatch(file, '*.json'):
         teams.append(file.split('.')[0])


def rotate_list(target_list, offset):
    """
    Takes a list and an integer and cycles the items in the list by
    the offset defined by the integer, wrapping as necessary.
    """
    offset = offset % len(target_list)
    return target_list[offset:] + target_list[:offset]


def load_list(team):
    """
    Takes a team as a string, and loads the JSON file for that team.
    """
    try:
        source = open(os.path.join(mypath, '%s.json' % team))
    except IOError:
        sys.exit("No %s.json file found! Exiting." % team)
    except:
        sys.exit("Error opening %s.json for reading. Exiting." % team)

    try:
        typelist = json.load(source)
    except:
        sys.exit("Error loading %s.json. Does it exist?" % team)

    return typelist

def output_list(admins):
    """
    Takes a list of tuples, one of which is a list of dictionaries and the
    other is a string.
    """
    team = admins[1]
    print("%s Team List:" % team.title())
    print(admins[0])
    return admins[0], team

def whos_up(admins):
    team = admins[1]
    print("%s Team Current on-call :" % team.title())
    print(rotate_list(admins[0], cycle)[0])
    return rotate_list(admins[0], cycle)[0], team

def main():
    print("mypath: %s" % mypath)
    for team in teams:
        admins=(load_list(team),team)
        whos_up(admins)
        output_list(admins)


    print("Done!")


if __name__ == '__main__':
    main()
