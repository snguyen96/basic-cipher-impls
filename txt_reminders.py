from twilio.rest import Client
from datetime import datetime
import keys
import time
import xml.etree.ElementTree as ET
import urllib.request

def get_current_time():
    full_time = str(datetime.now().time())
    full_time = full_time.split('.')
    formatted_time = full_time[0][:-3]
    return formatted_time

def remind_at_time(sender, receiver):
    information = input('enter a message: ')
    alert_time = input('enter a time: ')
    print(alert_time)
    
    while True:
        current_time = get_current_time()
        print(current_time)
        if alert_time == current_time:
            message = twilioCli.messages.create(body=information, from_=sender, to=receiver)
            break
        else:
            time.sleep(30)

def remind_bus_time(sender, receiver):
    while True:
        check_bus_time_home(sender, receiver)
        try:
            url = keys.url
            decoded_route = urllib.request.urlopen(url).read().decode('utf-8')
        except:
            print('error')
        
        bus = 'bus.xml'
        file = open(bus,'w')
        
        file.write(decoded_route)
        
        file.close()
        
        tree = ET.parse(bus)
        root = tree.getroot()
        
        for p in root.findall('predictions'):
            for directions in p.findall('direction'):
                for predictions in directions.findall('prediction'):
                    time_left = predictions.attrib['minutes']
                    information = time_left + " minutes until CM arrives to " + keys.a_location + "."
                    print("h" + time_left)
                    if time_left <= '10':
                        message = twilioCli.messages.create(body=information, from_=sender, to=receiver)
                        break
        
        time.sleep(120)
                    
def check_bus_time_home(sender, receiver):
    try:
        url = keys.url_home
        decoded_route = urllib.request.urlopen(url).read().decode('utf-8')
    except:
        print('error')
        
    bus = 'bus.xml'
    file = open(bus,'w')
    
    file.write(decoded_route)
    
    file.close()
    
    tree = ET.parse(bus)
    root = tree.getroot()
    
    for p in root.findall('predictions'):
        for directions in p.findall('direction'):
            for predictions in directions.findall('prediction'):
                time_left = predictions.attrib['minutes']
                information = time_left + " minutes until CM arrives to SITTERSON."
                print('S' + time_left)
                if time_left <= '15':
                    message = twilioCli.messages.create(body=information, from_=sender, to=receiver)
                    return 0
    
accountSID = keys.accountSID
authToken = keys.authToken

twilioCli = Client(accountSID, authToken)

myTwilioNumber = keys.myTwilioNumber
myNumber = keys.myNumber

remind_bus_time(myTwilioNumber, myNumber)