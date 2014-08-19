#!/usr/env/python

"""Update any column of text with a new version
In the case of the script so far, we employ a more thorough cleaning
to the rawtext column and update the text column
Only assumption is really that you have an ID field in the table
"""

import MySQLdb as mdb
import argparse
import enron
import createdb
import re
import logging
import pdb

parser = argparse.ArgumentParser("Update a column in an existing database")
parser.add_argument("-n", "--name", help = 'Database name', required = True, type = str)
parser.add_argument("-t", "--table", help = 'Table name', required = True, type = str)
parser.add_argument("-c", "--column", help = 'Column name', required = True, type =str)


def main():


    args = parser.parse_args()
    print args

    connection, cursor = enron.connectDB(args.name)

    
    cursor.execute("select ID from {0} order by id desc limit 1;".format(args.table))
    numrows = int(cursor.fetchone()[0])

    #loop over number of rows
    #this is less efficient than operating on the database as a whole
    #but it won't make your computer slow down and explode

    
    for id in range(1, numrows+1):
        
        #fetch the rawtext

        cursor.execute("""select rawtext from Emails where id = {0}""".format(id))
        rawtext = cursor.fetchone()[0]

        cleantext = enron.cleanString(rawtext)

        cleantext_escape = mdb.escape_string(cleantext)

        query = """UPDATE {0} set {1}='{2}' where `id` =  {3};""".format(args.table, args.column, cleantext_escape, id)
        
        cursor.execute(query)
        connection.commit()

        print 'Updated entry {0}'.format(id)


    connection.close()

if __name__ =='__main__':

    main()

