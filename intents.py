import json
from multiprocessing import Pool

import responses

import hypixel
import tools

FRIEND_DATA = json.loads(open('private/uuids.json').read())
FRIENDS = [hypixel.HypixelPlayer(x['uuid'], alias=x['alias']) for x in FRIEND_DATA]


def friend_list():
    pool = Pool(4)
    online_pairs = pool.map_async(tools.get_online, FRIENDS)
    online_pairs.wait()

    online = [x[1] for x in online_pairs.get() if x[0]]

    response = None
    if len(online) == 0:
        response = 'None of your friends are online.'
    elif len(online) == 1:
        response = f'{online[0]} is online.'
    elif len(online) > 1:
        response = f'{tools.english_list(online)} are online.'
    else:
        response = 'Something went wrong finding who is online.'

    response_object = responses.GoogleAssistantResponse(response)
    response_json = json.dumps(response_object)

    return response_json


INTENTS = {
    'friend list': friend_list
}

def get_response(request):
    intent_name = request['queryResult']['intent']['displayName']
    return str(INTENTS[intent_name]())


if __name__ == '__main__':
    print(friend_list())
