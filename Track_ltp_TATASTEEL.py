#import logging
#logging.basicConfig(level=logging.DEBUG)

import websocket
import pandas as pd
from time import sleep
import json
import csv
from login import *
from alice_blue import *

#access_token = AliceBlue.login_and_get_access_token(username='username', password='password', twoFA='twoFA',  api_secret='api_secret')

access_token="uRxG9AJbmQmTpCdK_TT8a-KTDsUhpgnEXjAv1WN5lFs.9edkFcimX8NL7Rf38sEMw2acSCAwxfbPB35asExq-RU"

alice = AliceBlue(username='username', password='password', access_token=access_token, master_contracts_to_download=['NSE', 'BSE'])


print(alice.get_profile()['data']['name']) # get profile name
print()

# Creating an dictionary for converting it into DataFrame
main_dic ={
    'exchange_time':[],
    'last_price':[]
      }


#  Start getting live feed via socket
socket_opened = False
def event_handler_quote_update(message):

    # Extracting ltp and exchange_time_stamp and store it in variable
    last_price = message['ltp']
    exchange_time = message['exchange_time_stamp']

    # Appending it to dictionary
    main_dic['exchange_time'].append(exchange_time)
    main_dic['last_price'].append(last_price)

# Converting dictionary into DataFrame
    df = pd.DataFrame(main_dic)
    df['exchange_time']  = pd.to_datetime(df['exchange_time'], unit='s')
    print(df)



def open_callback():
    global socket_opened
    socket_opened = True

alice.start_websocket(subscribe_callback=event_handler_quote_update,
                      socket_open_callback=open_callback,
                      run_in_background=True)

while(socket_opened==False):
    pass
alice.subscribe(alice.get_instrument_by_symbol('NSE', 'TATASTEEL'), LiveFeedType.MARKET_DATA)
sleep(10)  # This is not heartbeat message


'''
#   Unsubscribe to a live feed

alice.unsubscribe(alice.get_instrument_by_symbol('NSE', 'TATASTEEL'), LiveFeedType.MARKET_DATA)
'''
