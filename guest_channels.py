#!/usr/bin/env python

import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv('config.env')

slack_token = os.getenv('SLACK_TOKEN')
client = WebClient(token=slack_token)

def get_users(limit = 100, cursor = ''):
    try:
        resp = client.users_list(limit=limit, cursor=cursor)
    except SlackApiError as e:
        if e.response.status_code == 429:
            delay = int(e.response.headers['Retry-After'])
            print(f'Timeout: retry in {delay} seconds.')
            time.sleep(delay)
            get_users(limit = limit, cursor = cursor)
        else:
            print(f'{e.response}')

    return resp

def get_guest_users(guest_users = [], cursor = ''):
    resp = get_users(cursor=cursor)

    for member in resp['members']:
        if member.get('is_restricted', False):
            guest_users.append(member)

    next_cursor = resp['response_metadata']['next_cursor']

    if next_cursor:
        get_guest_users(guest_users = guest_users, cursor = next_cursor)

    return guest_users 

def get_users_conversations(user, channels = [], cursor = ''):
    resp = client.users_conversations(user = user, exclude_archived = True, cursor = cursor)
    channels.extend(resp['channels'])

    next_cursor = resp['response_metadata']['next_cursor']

    if next_cursor:
        get_users_conversations(user, channels, cursor = next_cursor)

    return channels

if __name__ == '__main__':
    guests = get_guest_users()
    for guest in guests:
      channel_list = get_users_conversations(user = guest['id'], channels = [])

      channel_names = []
      for channel in channel_list:
        channel_names.append(channel['name'])
      channel_names.sort()

      print(f'{guest["name"]}: {", ".join(str(x) for x in channel_names)}') 
