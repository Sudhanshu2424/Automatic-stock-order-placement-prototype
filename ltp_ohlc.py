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
username = 'AB086867'
password = 'chicu@24428'
access_token = 'vpAXcERNF3gV5y6j3p9pBfFMuyk8lCJiVFOz8nDpBzo.C5JD4YawenO1s3neMmw-K-B0H4qvQi91IABSwPBymsA'
alice = AliceBlue(username=username, password=password, access_token=access_token, master_contracts_to_download=['NSE','NFO','MCX'])


symbols = ['GOLD AUG FUT','SILVERM AUG FUT','COPPER AUG FUT']


#import datetime

while True:


	socket_opened = False
	def event_handler_quote_update(message):
    		print(datetime.datetime.now().time())
    		symbolName = message['instrument'].symbol
    		ltp = message['ltp']
    		print(f'{symbolName} -> {ltp}')

	def open_callback():
    		global socket_opened
    		socket_opened = True

	alice.start_websocket(subscribe_callback=event_handler_quote_update,
                      	socket_open_callback=open_callback,
                      	run_in_background=True)

	alice.subscribe([alice.get_instrument_by_symbol('MCX', name) for name in symbols],LiveFeedType.MARKET_DATA)
