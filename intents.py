import json
from multiprocessing import Pool

import responses

import hypixel
import splatoon
import tools

FRIEND_DATA = json.loads(open('private/uuids.json').read())
FRIENDS = [hypixel.HypixelPlayer(x['uuid'], alias=x['alias']) for x in FRIEND_DATA]

def friend_list(request):
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


def ruleset_get(request):
    requested_ruleset = request['queryResult']['parameters']['rulesets']
    blocks = splatoon.search_schedule(lambda x: x.ruleset[1], requested_ruleset)

    print(requested_ruleset, splatoon.RULESETS)

    stages_string = splatoon.stages_notification(blocks)
    ruleset_string = [x['name'] for x in splatoon.RULESETS if x['key'] == requested_ruleset][0]

    result = f'You can play {ruleset_string} in {stages_string}'

    return responses.GoogleAssistantResponse(result)


def schedule_get(request):
    pass


INTENTS = {
    'friend list': friend_list,
    'ruleset get': ruleset_get
}

def get_response(request):
    intent_name = request['queryResult']['intent']['displayName']
    return str(INTENTS[intent_name](request))


if __name__ == '__main__':
    pass
    # print(friend_list())
