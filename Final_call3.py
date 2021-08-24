import requests
from requests_oauthlib import OAuth2Session
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import os
import sys
from requests_oauthlib import OAuth2Session
from alice_blue import *
import datetime
import time
import pandas as pd


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
username = '*******'
password = '********'
access_token = 'vpAXcERNF3gV5y6j3p9pBfFMuyk8lCJiVFOz8nDpBzo.C5JD4YawenO1s3neMmw-K-B0H4qvQi91IABSwPBymsA'
alice = AliceBlue(username=username, password=password, access_token=access_token, master_contracts_to_download=['NSE','NFO','MCX'])


symbols = ['GOLD AUG FUT','SILVERM AUG FUT','COPPER AUG FUT']

price_15 = dict.fromkeys(symbols,0) # Creating Dictionary to store values at 9:15
price_30 = dict.fromkeys(symbols,list()) # Creating Dictionary to store values between 9:15 to 9:30

socket_opened = False
def event_handler_quote_update(message):

    if datetime.datetime.now().time() >= datetime.time(9,15):
        if datetime.datetime.now().time() <= datetime.time(9,15,20):
            symbolName = message['instrument'].symbol
            ltp = message['ltp']

            price_15[symbolName]=ltp # value at 9:15


    if datetime.datetime.now().time() > datetime.time(9,15):
        if datetime.datetime.now().time() < datetime.time(9,30):

        	symbolName = message['instrument'].symbol
        	ltp = message['ltp']

            price_30[symbolName].append(ltp) # Appending values between 9:15 to 9:30

    if datetime.datetime.now().time() > datetime.time(9,30):
        
        alice.unsubscribe([alice.get_instrument_by_symbol('MCX', name) for name in symbols],LiveFeedType.MARKET_DATA)

def open_callback():
	global socket_opened
	socket_opened = True

alice.start_websocket(subscribe_callback=event_handler_quote_update,
              	     socket_open_callback=open_callback,
                  	 run_in_background=True)


alice.subscribe([alice.get_instrument_by_symbol('MCX', name) for name in symbols],LiveFeedType.MARKET_DATA)

# Calculating Buy/Sell
for Symbol,Start_price in price_15.items():
    if Start_price < min(price_30[Symbol]):
        print('Buy ',Symbol)
    elif Start_price > max(price_30[Symbol]):
        print('Sell ',Symbol)
    else:
        print('Nothing ',Symbol)
