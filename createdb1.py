#/usr/env/python

"""Code to create the test_db from the Enron email data"""

import email as em
import os
import argparse
import MySQLdb as db

parser = argparse.ArgumentParser("Create database from email files")
parser.add_argument("startdir", type = str, help='Starting place for directory tree')

args = vars(parser.parse_args())


# Create function here to create the database with the required tables
# See:  http://zetcode.com/db/mysqlpython/


def emailList(startdir):
    """Create list of all emails (with their full directory address)"""
    found = []
    for dir,subdir,files in os.walk(startdir):
        for ff in files:
            found.append(os.path.join(dir,ff))
    return found


def getMetadata(message):
    """Retrieve metadata from an email."""
    efile = open(message, 'r')
    msg = em.message_from_file(efile)
    efile.close()
    From=msg['From']
    To=msg['To']
    Subject=msg['Subject']
    Date=msg['Date']
    # Insert command to pre-process the metadata here
    return (From,To,Subject,Date)


def getBodyText(message):
    """Retrieve the main body text from an email."""
    efile = open(message, 'r')
    msg = em.message_from_file(efile)
    efile.close()
    msg_text = msg.get_payload()
    # Insert command to pre-process the main body text here
    return msg_text



startdir = args['startdir']
emails=emailList(startdir)
for i in emails:
    meta=getMetadata(i)
    body=getBodyText(i)
    # Insert SQL 'insert' commands here to fill in the metadata and body text tables in the database 



    #TODO: create database to read data into before this
    #TODO: combine list of strings in msg_text into 1 long string. Easy enough with .join()
    #TODO: tidy this up 
