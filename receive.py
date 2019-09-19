#!/usr/bin/env python
#
# Very basic example of using Python 3 and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# This script is example code from this blog post:
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
# This is an updated version of the original -- modified to work with Python 3.4.
#
import sys
import imaplib
import getpass
import email
import email.header
import datetime


EMAIL_ACCOUNT = "johnasdoe.123456789@gmail.com"

# Use 'INBOX' to read inbox.  Note that whatever folder is specified, 
# after successfully running this script all emails in that folder 
# will be marked as read.
EMAIL_FOLDER = "INBOX"

def decryption(msg,k):
        ct = str(msg)
        pt = ""
        for x in ct:
                if ord(x)>=65 and ord(x)<=90 :
                        pt = pt + chr((((ord(x)-65)-k)%26)+65)
                elif x>='a' and x<='z' :
                        pt = pt + chr((((ord(x)-97)-k)%26)+97)
                else :
                        pt = pt + x
        return pt


def get_decoded_email_body(raw_email,k):
    raw_email_string = raw_email.decode('utf-8')
    # converts byte literal to string removing b''
    email_message = email.message_from_string(raw_email_string)
    # this will loop through all the available multiparts in mail
    for part in email_message.walk():
     if part.get_content_type() == "text/plain": # ignore attachments/html
      body = part.get_payload(decode=True)
      msg = body.decode('utf-8')
      pt = decryption(msg,k)
      #print("Encrypted Text was = \n",msg)
      #print("Decrypted Text is = \n",pt)
      print(pt)
      
     else:
      continue

def process_mailbox(M):
    #"""
    #Do something with emails messages in the folder.  
    #For the sake of this example, print some headers.
    #"""

    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        subject = str(hdr)
        key = int(subject)
        print ('Key = ',key)
        print ('Message %s: %s' % (num, subject))
        print ('Raw Date:', msg['Date'])
        # Now convert to local date-time
        #date_tuple = email.utils.parsedate_tz(msg['Date'])
        #if date_tuple:
        #    local_date = datetime.datetime.fromtimestamp(
        #        email.utils.mktime_tz(date_tuple))
        #   print ("Local Date:", \
        #        local_date.strftime("%a, %d %b %Y %H:%M:%S"))
        get_decoded_email_body(data[0][1],key)
        print("Done\n\n")


M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    rv, data = M.login(EMAIL_ACCOUNT, "2132845042")
except imaplib.IMAP4.error as e:
    print (str(e))
    print ("LOGIN FAILED!!! ")
    sys.exit(1)

print(rv, data)

rv, mailboxes = M.list()
if rv == 'OK':
    print("Mailboxes:")
    print(mailboxes)

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print("Processing mailbox...\n")
    process_mailbox(M)
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

M.logout()
