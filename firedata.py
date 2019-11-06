from firebase import firebase  
import time
from datetime import datetime
import random
import sys

from Adafruit_IO import MQTTClient
import requests


ADAFRUIT_IO_KEY      = 'a08359a987094685ba743b5d89ccfb35'       
ADAFRUIT_IO_USERNAME = 'vesitgroup6'  
                                                    
                                        
def connected(client):
    
    print('Connected. Listening changes...')    
    client.subscribe('bulb')


def disconnected(client):
    
    print('Disconnected !')
    sys.exit(1)


def message(client, feed_id, status):
    global st, sd, sday, st1, oncommand
    if feed_id == 'bulb':
        if status=='1':
            st = datetime.now().strftime('%H:%M:%S')
            sd = datetime.now().strftime('%Y:%m:%d')
            sday = int(datetime.now().strftime('%d'))
            st1 = time.time()
            oncommand = "Bulb ON"
            print("{} : {} {} {} {}".format(oncommand,sd,st,sday,st1))
            
            
        else:
            et = datetime.now().strftime('%H:%M:%S')
            ed = datetime.now().strftime('%Y:%m:%d')
            eday = int(datetime.now().strftime('%d'))
            et1 = time.time()
            offcommand = "Bulb OFF"
            timediff = et1 - st1
            print("{} : {} {} {} {}".format(offcommand,ed,et,eday,et1))
            print(timediff)
            from firebase import firebase

            firebase = firebase.FirebaseApplication('https://vesitiot.firebaseio.com/', None)  

            data =  { 'start_date': sd,
                      'start_time': st,
                      'start_day': sday,
                      'stn': st1,  
                      'oncommand': oncommand,
                      'end_date': ed,
                      'end_time': et,
                      'end_day': eday,
                      'etn': et1,  
                      'offcommand': offcommand,
                      'timediff': timediff,
                    }  
            result = firebase.post('/start_data/',data)  
            print(result)
            

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message


client.connect()


client.loop_blocking()
