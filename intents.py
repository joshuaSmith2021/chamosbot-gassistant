import datetime
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

    stages_string = splatoon.stages_notification(blocks)
    ruleset_string = [x['name'] for x in splatoon.RULESETS if x['key'] == requested_ruleset][0]

    result = f'You can play {ruleset_string} in {stages_string}'

    return responses.GoogleAssistantResponse(result)


def schedule_now(request):
    current_stages = splatoon.get_current_stages()
    stages_string = splatoon.stages_notification(current_stages, include_ruleset=True,
                                                 include_stage=True, include_time=False)

    result = f'Here\'s what\'s available: {stages_string}.'

    return responses.GoogleAssistantResponse(result)


def salmon_weapons_get(request):
    current_salmon_stages = splatoon.get_salmon_schedule()
    current = splatoon.SalmonScheduleItem(current_salmon_stages['details'][0])

    weapon_string = tools.english_list(map(str, current.weapons))

    time_string = None
    if datetime.datetime.now() < current.end:
        time_string = current.end.strftime('until %B %-d at %-I:%M%p')
    else:
        time_string = current.end.strftime('starting on %B %-d at %-I:%M%p')

    result = f'You can use the {weapon_string}, {time_string}.'

    return responses.GoogleAssistantResponse(result)


INTENTS = {
    'friend list': friend_list,
    'ruleset get': ruleset_get,
    'schedule now': schedule_now,
    'salmon weapons get': salmon_weapons_get
}

def get_response(request):
    intent_name = request['queryResult']['intent']['displayName']
    return str(INTENTS[intent_name](request))


if __name__ == '__main__':
    print(salmon_weapons_get(None))
