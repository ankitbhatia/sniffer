#!/usr/bin/python

import sys   #for cmd line argv
import os
import time    #for delay
import pygst   #for playing mp3 stream
import gst   # " "
import urllib2


#take command line args as the input string
input_string = sys.argv
#remove the program name from the argv list
input_string.pop(0)

#convert to google friendly url (with + replacing spaces)
tts_string = '+'.join(input_string)

print tts_string
google_translate_url = 'http://translate.google.com/translate_tts'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]

response = opener.open(google_translate_url+'?q='+tts_string+'&tl=en')
ofp = open('speech_google.mp3','wb')
ofp.write(response.read())
ofp.close()
os.system('mpg123 ' + 'speech_google.mp3')
