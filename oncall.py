#! /usr/bin/env python

"""
On Call Rotator - Less-Goldbergian Edition.
"""

import sys, os, datetime
import simplejson as json

mypath = os.path.abspath(os.path.dirname(__file__))


#today = datetime.datetime.now() # Got the current time
today = datetime.datetime(2017, 2, 9, 15, 0, 20, 912320) # Fuuuuuture!

week = int(today.strftime('%U')) # Converted to a numeric week number
weeks_per_cycle = 2  # Edit this to control how long each person is on-call.
cycle = int(week / weeks_per_cycle) # What cycle number are we on?
groups = ("system", "network", "mobility") # Each of these should have a <group>admins.json file

# app = Flask(__name__)


def rotate_list(target_list, offset):
    """
    Takes a list and an integer and cycles the items in the list by
    the offset defined by the integer, wrapping as necessary.
    """
    offset = offset % len(target_list)
    return target_list[offset:] + target_list[:offset]


def load_list(kind):
    """
    Takes a string, and loads the JSON file for that kind of admin.
    """
    try:
        source = file(os.path.join(mypath ,'%sadmins.json' % kind))
    except IOError:
        sys.exit("No %sadmins.json file found! Exiting." % kind)
    except:
        sys.exit("Error opening %sadmins.json for reading. Exiting." % kind)

    try:
        typelist = json.load(source)
    except:
        sys.exit("Error loading %sadmins.json. Does it exist?" % kind)

    return typelist

def output_list(admins):
    """
    Takes a list of tuples, one of which is a list of dictionaries and the
    other is a string.
    """
    kind = admins[1]
    print "%sadmins List:" % kind.title()
    print admins[0]
    return admins[0], kind

def whos_up(admins):
    kind = admins[1]
    print "%sadmins Current on-call :" % kind.title()
    print rotate_list(admins[0], cycle)[0]
    return rotate_list(admins[0], cycle)[0], kind

def main():
    print "mypath: %s" % mypath
    for kind in groups:
        admins=(load_list(kind),kind)
        whos_up(admins)
        output_list(admins)


    print "Done!"


if __name__ == '__main__':
    main()
