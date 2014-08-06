#/usr/env/python

"""Code to create the test_db from the Enron email data"""

import email
import os
import argparse
import mysqldb as db


def main():

    parser = argparse.ArgumentParser("Create database from email files")
    parser.add_argument("startdir", type = str, help='Starting place for directory tree')

    args = vars(parser.parser_args())

    #start directory is unique for each person

    startdir = args['startdir']

    found = []

    for dir,subdir,files in os.walk(startdir):

        for ff in files:

            found.append(os.path.join(dir,ff))

    for message in found:

        #create email object from the file list.  Process each one then send to DB

        efile = open(message, 'r')
        msg = email.message_from_file(efile)
        efile.close()

        msg_text = msg.get_payload()

    #TODO: create database to read data into before this
    #TODO: combine list of strings in msg_text into 1 long string. Easy enough with .join()
    #TODO: tidy this up 




if __name__ == '__main__':
    main()