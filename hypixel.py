import json
import random

import requests

import mojang

API_KEYS = json.loads(open('private/auth.json').read())['hyapi_keys']

def get_key():
    return random.choice(API_KEYS)


def get_player_stats(uuid):
    url = f'https://api.hypixel.net/player?key={get_key()}&uuid={uuid}'
    req = requests.get(url)
    return req.json()


def get_player_status(uuid):
    key = get_key()
    url = f'https://api.hypixel.net/status?key={key}&uuid={uuid}'
    req = requests.get(url)
    return req.json()


class HypixelPlayer(mojang.Player):
    def is_online(self):
        status = get_player_status(self.uuid)['session']['online']
        return status


if __name__ == '__main__':
    print(HypixelPlayer('a1bc77a1a24342d29ada5684756a358c').is_online())

