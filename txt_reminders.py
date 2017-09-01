from twilio.rest import Client
from datetime import datetime
import keys
import time

def get_current_time():
    full_time = str(datetime.now().time())
    full_time = full_time.split('.')
    formatted_time = full_time[0][:-3]
    return formatted_time

accountSID = keys.accountSID
authToken = keys.authToken

twilioCli = Client(accountSID, authToken)

myTwilioNumber = keys.myTwilioNumber
myNumber = keys.myNumber

information = input('enter a message: ')
alert_time = input('enter a time: ')
print(alert_time)

while True:
    current_time = get_current_time()
    print(current_time)
    if alert_time == current_time:
        message = twilioCli.messages.create(body=information, from_=myTwilioNumber, to=myNumber)
        break
    else:
        time.sleep(30)