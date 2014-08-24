# mopitwail.py 0.1
# piratesec.de
#!/usr/bin/python

import subprocess
import datetime
import time
from time import sleep
import os
import sys
import random
# Mail-Imports
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Tweet-Imports
import tweepy
import tweetpony
# GPIO-Import
import RPi.GPIO as GPIO
import time

# --------- Config ---------
GPIO.setmode(GPIO.BCM)
GPIO_PIR = 7
GPIO.setup(GPIO_PIR,GPIO.IN)
curr  = 0
prev = 0
api = tweetpony.API(consumer_key = "XXX", consumer_secret = "XXX", access_token = "XXX", access_token_secret = "XXX")
tweettext = "Intruder detected"

# --------- Funktionen ---------
def takepic():
    print "taking pic..."
    grab_cam = subprocess.Popen("sudo fswebcam -r 1920x1080 -d /dev/video0 -q /home/pi/projects/tweepic/pictures/%d.%m.%Y-%H:%M.jpg", shell=True)
    grab_cam.wait()
    # prep the pic.
    todays_date = datetime.datetime.today()
    image_name = todays_date.strftime('%d.%m.%Y-%H:%M')
    image_path = '/home/pi/projects/tweepic/pictures/' + image_name + '.jpg'
    pic = image_path
    print "pic taken."
    return todays_date, image_path, pic

def tweeter(todays_date, image_path):
    print "tweeting pic and this text: %s" % tweettext
    try:
        api.update_status_with_media(status = (tweettext, todays_date.strftime('%d.%m.%Y-%H:%M')), media= image_path)
        print "getweetet."
    except tweetpony.APIError as err:
            print "Twitter error #%i: %s" % (err.code, err.description)
            # del_img = subprocess.Popen("sudo rm -rf  " + image_path, shell=True)
            # del_img.wait()
            time.sleep(1)

def mailer(pic):
    print "mailing pic to: XXX"
    sender = "XXX"
    empfaenger = "XXX"
    s = smtplib.SMTP('XXX')
    s.starttls()
    s.ehlo()
    s.login('XXX', 'XXX')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Intruder detected'
    msg['From'] = "XXX"
    msg['To'] = empfaenger

    text = "Pic of intruder"
    fp = open(pic, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    msg['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime())
    msg['User-Agent'] = "PyLucid (Python v2.7)"
    s.sendmail(sender, empfaenger, msg.as_string())
    print "pic mailed."

# --------- Main ---------
try:
    while GPIO.input(GPIO_PIR)==1:
        curr  = 0
    print "Scanning..."
    while True :
        curr = GPIO.input(GPIO_PIR)
        # MOTION DETECTED
        if curr==1 and prev==0:
            print "Motion detected! taking 3 pics"
            count = 0
            while count < 3:
                todays_date, image_path, pic = takepic() # take pic
                tweeter(todays_date, image_path) # tweet
                mailer(pic) # mail
                count += 1

            time.sleep(15)
            # Record previous state
            prev=1

        elif curr==0 and prev==1:
            prev=0
            print "Scanning..."
        time.sleep(0.01)

except KeyboardInterrupt:
    print "  Quit"
    GPIO.cleanup()
