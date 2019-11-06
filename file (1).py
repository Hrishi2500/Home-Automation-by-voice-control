
import random
import sys
import time
import RPi.GPIO as io

from Adafruit_IO import MQTTClient


import requests



ADAFRUIT_IO_KEY      = 'a4ab768e33124b39a52c396fbbd2b8b0'       
ADAFRUIT_IO_USERNAME = 'hhdeshpande25'  
                                                    
                                        


io.cleanup()
io.setmode(io.BCM)
io.setwarnings(False)


io.setup(18,io.OUT)
io.output(18, io.HIGH)
io.setup(12,io.OUT)
io.output(12, io.HIGH)

def connected(client):
    
    print('Connected. Listening changes...')
    
    client.subscribe('bulb')
    client.subscribe('fan')
    


def disconnected(client):
    
    print('Disconnected !')
    sys.exit(1)

def message(client, feed_id, status):
    
    
    if feed_id == 'bulb':
        if status=='1':
            print("Bulb ON")
            st = time.time()
            io.output(18,io.LOW)
            time.sleep(10)
        else:
            print("Bulb OFF")
            io.output(18,io.HIGH)
            
    
    if feed_id == 'fan':
        io.output(12, io.HIGH)
        if status=='1':
            print("Fan ON")
            io.output(12,io.LOW)
        else:
            print("Fan OFF")
            io.output(12,io.HIGH)
    
    
        #requests.post('{0}/widgets/slider'.format(DASHBOARD_URL), data={'value': payload})
    #elif feed_id == 'pi-dashboard-humidity':
        #requests.post('{0}/widgets/humidity'.format(DASHBOARD_URL), data={'value': payload})
    #elif feed_id == 'pi-dashboard-temp':
        #requests.post('{0}/widgets/temp'.format(DASHBOARD_URL), data={'value': payload})



client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message


client.connect()


client.loop_blocking()