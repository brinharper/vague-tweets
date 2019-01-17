# MIT Computational Cognitive Science Group
# Author: Brin Harper

import os
import json
import requests
from datetime import datetime
from collections import namedtuple

darksky_key = open("darksky.key").read()

geo_key = open("geocoder.key").read()
os.environ["GOOGLE_API_KEY"] = geo_key
import geocoder

''' Retrieve temp at a given location and date '''
Temperature = namedtuple('Temperature', 'current high low')
def get_historical_temp(lat, long, dt):
    time = datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S")
    #DarkSky request format: https://api.darksky.net/forecast/[key]/[latitude],[longitude],[time]
    url = "https://api.darksky.net/forecast/{}/{},{},{}?exclude=hourly,flags".format(darksky_key, lat, long, time)
    response = requests.get(url).json()
    current_temp = response['currently']['temperature']
    daily_high = response['daily']['data'][0]['temperatureHigh']
    daily_low = response['daily']['data'][0]['temperatureLow']
    return Temperature(current=current_temp, high=daily_high, low=daily_low)

''' Estimate coordinates based on user's location description '''
def geocode(tweet):
    location = tweet["user"]["location"]
    geo = geocoder.google(location)
    latlng = geo.latlng
    return latlng

# TODO: more work on filtering out bogus locations
''' Call process on your tweet to get the associated weather '''
def process(tweet):
    latlng = geocode(tweet)
    date = tweet['created_at']
    dt = datetime.strptime(date, "%a %b %d %H:%M:%S +0000 %Y")
    temps = get_historical_temp(latlng[0], latlng[1], dt)
    print("Current temperature: " + str(temps.current) + " degrees F")
    print("Daily high: " + str(temps.high) + " degrees F")
    print("Daily low: " + str(temps.low) + " degrees F")
    return temps

if __name__ == '__main__':
    tweet = json.load(open("sample_tweet.json"))
    process(tweet)
