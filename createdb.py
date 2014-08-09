#/usr/env/python

"""Code to create the test_db from the Enron email data"""

import email
import os
import argparse
import MySQLdb as mdb
import __future__

parser = argparse.ArgumentParser("Create database from email files")
parser.add_argument("startdir", type = str, help='Starting place for directory tree', dest='startdir')


def create_db():

    """Creates connection to mysql and creates the DB in standard form"""

    #connect to local server with following usernames

    connection = mdb.connect('localhost', 'kpmg1', 's2ds')
    cursor=connection.cursor()


    #DB schema. We can amend this however we want as we go.
    #I've written everything as 1 table as that seemed the easiest, but
    # if we want to create more tables that's easy.  Just do:
    # TABLES['newname']= and fill in the new columns in the same format
    #I've added a local file location to be helpful during debugging/creation

    DB_NAME='enron'
    TABLES={}
    TABLES['emails'] = (

        "CREATE TABLE `emails` ("
        "  `id` INT NOT NULL AUTO_INCREMENT,"
        "  `from` varchar(100) NOT NULL,"
        "  `to` varchar(1000) NOT NULL,"
        "  `subject varchar(200),"
        "  `date` date NOT NULL,"
        "  `cc` varchar(1000),"
        "  `bcc` varchar(1000),"
        "  `rawtext` varchar(15000) NOT NULL,"
        "  `text` varchar(15000) NOT NULL,"
        "  `fileloc` varchar(100) NOT NULL"
        "  PRIMARY KEY (id)"
        ") ENGINE=InnoDB;")

    #try to create. If not raise exception and exit

    try:

        cursor.execute("CREATE DATABASE {0} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))

    except mysql.connector.Error as err:

        print ("Failed creating database",format(err))
        return

    #Try to crate databse

    for name,ddl in TABLES.iteritems()

        try:

            print ("Creating table {0}: \n".format(name))
            cur.execute(ddl)

        except mysql.connector.Error as err:

            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:

                print ("Table {0} already exists".format(name))
            else:
                print (err.msg)


    if connection:
        conection.close()

    #Close the empty database if it is created correctly

    return


def deleteDB(cur, tablename):

    cur.execute("""DROP TABLE IF EXISTS {0}""".format(tablename))
    return

def connectDB(db):

    connection = mdb.connect('localhost', 'kpmg1', 's2ds', db)
    cursor=connection.cursor()

    return (connection,cursor)



def addDBEntry(cur, tablename, email, filepath):

    from = email['From']
    to = email['To']
    cc = email['X-cc']
    bcc=email['X-bcc']
    subject=email['Subject']
    date = email['Date']
    localfile = filepath
    rawtext = email.get_payload()
    cleantext = cleanMessage(rawtext)


def cleantext(message):

    #remove \n

    message = re.sub(r'\n', '', message)

    #remove



def main():
 

    #First thing: create the DB

    createDB()
    connection, cursor = connectDB('enron')



    #start directory is unique for each person

    startdir = args.startdir

    found = []

    for dir,subdir,files in os.walk(startdir):

        for ff in files:

            found.append(os.path.join(dir,ff))

    for message in found:

        #create email object from the file list.  Process each one then send to DB

        with open(message, 'r') as efile:
            msg = email.message_from_file(efile)
        

        addDBEntry(curson, 'emails', msg, message)

    #TODO: create database to read data into before this
    #TODO: combine list of strings in msg_text into 1 long string. Easy enough with .join()
    #TODO: tidy this up 




if __name__ == '__main__':
    main()
