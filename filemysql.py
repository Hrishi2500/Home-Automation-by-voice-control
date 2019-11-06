import time
from datetime import datetime
import mysql.connector
import random
import sys
import time
import RPi.GPIO as io

from Adafruit_IO import MQTTClient

import requests



ADAFRUIT_IO_KEY      = 'a4ab768e33124b39a52c396fbbd2b8b0'       
ADAFRUIT_IO_USERNAME = 'hhdeshpande25'  
                                                    
                                        
def starttime():
    start_time = datetime.now().strftime('%H:%M:%S')
    print(start_time)
    return start_time


def startdate():
    start_date = datetime.now().strftime('%Y:%M:%D')
    print(start_date)
    return start_date


def endtime():
    end_time = datetime.now().strftime('%H:%M:%S')
    print(end_time)
    return end_time

def enddate():
    end_date = datetime.now().strftime('%Y:%M:%D')
    print(end_date)
    return end_date

def dbconn(mydb):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="iot"
            )

    return 

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
            st = starttime()
            sd = startdate()
            dev_status = "Bulb ON"
            print(dev_status)
            st1 = time.time()
            io.output(18,io.LOW)
            time.sleep(10)
        else:
            io.output(18,io.HIGH)
            time.sleep(1)
            et = endtime()
            ed = enddate()
            dev_status1 = "Bulb OFF"
            print(dev_status1)

            et1 = time.time()

            exet = et1 - st1

            print(exet)
            
            mycursor = mydb.cursor()

            sql = "INSERT INTO file (start_date, start_time, oncommand, end_date, end_time, offcommand, device_period) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (sd, ,st, dev_status, sd, et, dev_status1, exet)

            mycursor.execute(sql, val)

            mydb.commit()

            print(mycursor.rowcount, "record inserted.")
            
            
            
    
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
