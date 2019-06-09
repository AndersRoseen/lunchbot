#!/usr/bin/env python3
# coding: utf-8

import urllib2
from urllib2 import URLError, HTTPError
import urllib
import json
import sys
import re

# Get lunch from fazer site
## Test URL: http://jsonplaceholder.typicode.com/todos/1
lunch_url_week = 'https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fwww.fazerfoodco.se%2Fmodules%2FMenuRss%2FMenuRss%2FCurrentWeek%3FcostNumber%3D6446%26language%3Dsv'
lunch_url_day = 'https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fwww.fazerfoodco.se%2Fmodules%2FMenuRss%2FMenuRss%2FCurrentDay%3FcostNumber%3D6446%26language%3Dsv'
#print('Getting lunch...')
response = urllib2.urlopen(lunch_url_day)
#print('Got lunch!')

contents_json = response.read()
contents = json.loads(contents_json)

if (contents["status"] != 'ok'):
    print('Failed to get lunch')
    sys.exit()

today_day = contents["items"][0]["title"]
today = contents["items"][0]["description"]

if (today == ''):
    print('No lunch served today')
    sys.exit()

today_text = re.sub("<.*?>", "", today).replace('&amp;','&').replace('pannkakor','pannkakor :pancakes:')
rows = today_text.split("\n")
for i in range(len(rows)-1):
    if ('DAGENS VEG' in rows[i]):
        food_veg = rows[i+1]
    if ('DAGENS K' in rows[i]): # KÖTT
        food_meat = rows[i+1]
    if ('DAGENS FISK' in rows[i]):
        food_fish = rows[i+1]
    if ('DAGENS SOPPA' in rows[i]):
        food_soup = rows[i+1]

try:
    food_veg
    food_meat
    food_fish
    food_soup
except NameError:
    print('No lunch served today')
    sys.exit()

#print('VEG: ' + food_veg + '\n' + 'MEAT: ' + food_meat + '\n' + 'FISH: ' + food_fish + '\n' + 'SOUP: ' + food_soup)

# Post lunch to Slack channel #lunch
#webhook_url = 'https://hooks.slack.com/services/###' # Post to #test
webhook_url = 'https://hooks.slack.com/services/###' # Post to #lunch
slack_data = { "attachments": [
        {
#            "pretext": "*Idag serveras det:*",
            "text": ":cow: " + food_meat + "\n :broccoli: " + food_veg + "\n :tropical_fish: " + food_fish + "\n :bowl_with_spoon: " + food_soup,
            "mrkdwn_in": [
                "text",
                "pretext"
            ],
			"color": "#000099",
			"footer": "Saluhallen " + today_day,
           "footer_icon": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcST9L1Gdm-WHP_Fvl6Oi1ZBMk7uXesk3zhe8Aq_xJPl-NBQh9Wxfw"
        }
    ]}
headers = {'Content-type': 'application/json'}

data_json = json.dumps(slack_data)
req = urllib2.Request(webhook_url, data_json, headers) # Including data will create a POST request

print(data_json)

try:
    post_response = urllib2.urlopen(req)
except HTTPError as e:
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
except URLError as e:
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason


