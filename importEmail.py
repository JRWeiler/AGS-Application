import json
import datetime
import re
import os
import shutil
from subprocess import Popen
import math
import collections
import smtplib
import getpass  
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage



#Takes two arrays of imported records and 
def send_mail(imported, name):
    now = datetime.datetime.now()
    fromaddr = 'ADDRESS@MAIL.COM'
    toaddrs  = 'ADDRESS@MAIL.COM'
    msg = MIMEMultipart('related')
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg['Subject'] = name + " Imports: " + str(now.month) + "-" + str(now.day) + "-" + str(now.year) 
    body =  MIMEText("<p>Generated E-mail Text </p>"+ str(now.month) + "-" + str(now.day) + "-" 
    	+ str(now.year)+"<h2>"+name+" Imports</h2><br><h3>"
    	+ "<b>Imported</b><ul>"
    	+ str(imported)  
    	, 'html')
    msg.attach(body)
	
    server = smtplib.SMTP('webmail.DOMAIN.COM:25')

	
    #username =  fromaddr
    #password =  getpass.getpass("Password: ")
    
    #login(server, username, password)


    text = msg.as_string() 
    server.sendmail(fromaddr, toaddrs, text)  
    server.quit() 