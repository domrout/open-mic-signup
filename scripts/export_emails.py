"""
Get email addresses from the database and export them one per line
"""

import data.performer as performer
from data import Session

import sys


if len(sys.argv) != 2:
    print "Please enter a filename to which to save the email addresses"
else:
    print "Saving to %s" % sys.argv[1]

    with open(sys.argv[1], "w") as f:
        session = Session()

        query = session.query(performer.Performer).all()

        for _performer in query:
            print >> f, _performer.email
