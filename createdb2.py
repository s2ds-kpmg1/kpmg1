#/usr/env/python

"""Code to create the test_db from the Enron email data"""

#from __future__ import print_function
import email as em
import os,sys
import argparse
import MySQLdb as mdb


###  Command sequence to create database in Terminal (do this first):
# mysql -u root -p
# create database testdb;
# create user 'testuser'@'localhost' identified by 'test623';
# use testdb;
# grant all on testdb.* to 'testuser'@'localhost';
# quit;


### This code is to test that you can connect from this script to the database created by the Terminal code above. It should output something like
###    "Database version : 5.5.38-0ubuntu0.14.04.1"
# try:
#     con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');
#     cur = con.cursor()
#     cur.execute("SELECT VERSION()")
#     ver = cur.fetchone()
#     print "Database version : %s " % ver
# except mdb.Error, e:
#     print "Error %d: %s" % (e.args[0],e.args[1])
#     sys.exit(1)
# finally:    
#     if con:    
#         con.close()


# Run this code by on (for example) the allem-p directory of emails as:
# python createdb2.py /home/ilan/Desktop/test/allen-p


parser = argparse.ArgumentParser("Create database from email files")
parser.add_argument("startdir", type = str, help='Starting place for directory tree')

args = vars(parser.parse_args())


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
    From=str(msg['From']).replace('\r\n\t','')
    To=str(msg['To']).replace('\r\n\t','')
    Subject=str(msg['Subject']).replace('\r\n\t','').replace('"','')
    Date=str(msg['Date']).replace('\r\n\t','')
    metadata=(From, To, Subject, Date)
    return metadata


# Main body text will require considerable pre-processing and scrubbing.
# Part of the noise ('\\n\\n', '=020', etc) may be down to text encoding issues, either when we import them, or when they were exported to text. Either way we need to figure out how important it is to remove them, and decide how long we want to spend trying to remove them and when to stop.

# Text ncoding issues are explained here:
#  http://www.joelonsoftware.com/articles/Unicode.html

# Need to sort out the issue (i.e. eliminate) of text duplication amongst emails!! (e.g. text repeated in reply emails). This could skew everything so is crucial

# Tutorials on email parsing in Python:
#  http://www.smipple.net/snippet/IanLewis/Multipart%20Mail%20Processing%20in%20Python
# http://blog.magiksys.net/parsing-email-using-python-content
# http://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python
# https://www.inkling.com/read/programming-python-mark-lutz-4th/chapter-13/email-parsing-and-composing

def getBodyText(message):
    """Retrieve the main body text from an email."""
    efile = open(message, 'r')
    msg = em.message_from_file(efile)
    efile.close()
    #if msg.is_multipart():
    #    print "A multipart email has been found!"
        #Take care as parsing of the following email may be incorrect: {0}".format(message)
    msg_text = msg.get_payload()
    msg_text = "".join(msg_text).replace('"','')
    # Insert command to pre-process the main body text here
    return msg_text



# Read each email file and dump the metadata and the main body texts into two separate arrays.
startdir = args['startdir']
emails=emailList(startdir)
metatable=[]
texttable=[]
for i in emails:
    meta=getMetadata(i)
    metatable.append(meta)
    body=getBodyText(i)
    texttable.append(body)
 

# Insert table entries into mySQL database
con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Metadata")
    cur.execute("CREATE TABLE `Metadata`(Id INT PRIMARY KEY AUTO_INCREMENT, `From` TEXT NULL, `To` TEXT NULL, `Subject` TEXT NULL, `Date` TEXT Null) ENGINE=InnoDB DEFAULT CHARSET=latin1")
    for i in range(0,len(metatable)):
        metastring='INSERT INTO Metadata(`From`, `To`, `Subject`, `Date`) VALUES('+'"'+str(metatable[i][0])+'", "'+str(metatable[i][1])+'", "'+str(metatable[i][2])+'", "'+str(metatable[i][3])+'")'
        cur.execute(metastring)
        #print("Inserted element 0 to {0} into the metadata database.".format(i), end='\r')
        #print()
    cur.execute("DROP TABLE IF EXISTS `Text`")
    cur.execute("CREATE TABLE `Text`(Id INT PRIMARY KEY AUTO_INCREMENT, `body` LONGTEXT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1")
    for i in range(0,len(texttable)):
        textstring='INSERT INTO Text(`body`) VALUES('+'"'+str(texttable[i])+'")'
        cur.execute(textstring)
        #print("Inserted element 0 to {0} into the body text database.".format(i), end='\r')
        #print()


con.close()
    

