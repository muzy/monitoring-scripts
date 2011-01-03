#!/usr/bin/env python
#
# icinga_mail.py Script for Icinga Mail
# (c) Sebastian Muszytowski <sebastian@muszytowski.net>

import os
from optparse import OptionParser
import sys
import smtplib
from email.mime.text import MIMEText

parser = OptionParser()
parser.add_option("-f","--from",dest="sender",help="This sets the sender of the E-Mail",metavar="user@example.com")
parser.add_option("-H","--host",dest="host",help="(optional) This sets SMTP host. The default is 'localhost'",metavar="HOST",default="localhost")
parser.add_option("-u","--user",dest="user",help="(optional) This sets the username for SMTP authentication.",metavar="USER")
parser.add_option("-p","--password",dest="password",help="(optional) This sets the password for SMTP authentication. ",metavar="PASSWORD")
parser.add_option("--ssl",dest="ssl",help="(optional) If set, the connection will be a SSL-Connection. The default is a non-ssl connection.",default=False)
parser.add_option("--tls","--starttls",dest="starttls",help="(optional) If set starttls is used. This is off by default.",default=False)
parser.add_option("--port",dest="port",help="(optional) If set, the port is overwritten. The port defaults to 25",default=25)
parser.add_option("-s","--subject",dest="subject",help="This sets the SUBJECT of the mail.",metavar="SUBJECT")
parser.add_option("-b","--body",dest="body",help="This sets the BODY of the mail. If not set, it will be read from STDIN!",metavar="BODY")
parser.add_option("-t","--to",dest="to",help="Address where the mail is send to.",metavar="user@example.com")

(options,args) = parser.parse_args()

if (not options.sender or not options.subject or not options.to):

    print "You have to specify the sender (-f,--from) and the subject (-s,--subject) and the reciever (-t,--to)"

if ((options.user == None and options.password != None) or (options.user != None and options.user == None)):

    print "You have to specify both: username and password! Hint: use \"\" for an empty password!"

else:

    if options.ssl:
        server = smtplib.SMTP_SSL(options.host,options.port)
    else:
        server = smtplib.SMTP(options.host,options.port)

    if options.starttls:
        server.starttls()

    if (options.user != None and options.password != None):
        server.login(options.user,options.password)

    if (options.body != None):
        msg = MIMEText(options.body)
    else:
        msg = MIMEText(sys.stdin.read())

    msg['Subject'] = options.subject
    msg['From'] = options.sender
    msg['To'] = options.to

    server.sendmail(options.sender,[options.to],msg.as_string())
    server.quit()

