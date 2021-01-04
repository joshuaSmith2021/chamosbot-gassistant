import datetime
import json

import requests

BASE_URL = 'https://app.splatoon2.nintendo.net'

class Stage:
    name = None
    sid = None

    def __init__(self, data):
        self.name = data['name']
        self.sid = data['id']

    def __str__(self):
        return self.name


class ScheduleItem:
    ruleset = None
    gamemode = None
    stages = []
    start = None
    end = None

    def __init__(self, entry):
        self.ruleset = (entry['rule']['name'], entry['rule']['key'])
        self.gamemode = (entry['game_mode']['name'], entry['game_mode']['key'])
        self.stages = [Stage(x) for x in [entry['stage_a'], entry['stage_b']]]
        self.start = datetime.datetime.fromtimestamp(int(entry['start_time']))
        self.end = datetime.datetime.fromtimestamp(int(entry['end_time']))

    def time_range(self):
        time_format = '%b %-d %-I:%M%p'
        return f'{self.start.strftime(time_format)} – {self.end.strftime(time_format)}'

    def __str__(self):
        gamemode = self.gamemode[0]
        ruleset = self.ruleset[0]
        stages = ' & '.join(map(str, self.stages))
        time_range = self.time_range()
        return f'{gamemode} {ruleset} on {stages} at {time_range}'

    def __repr__(self):
        return self.__str__()


def get_schedule():
    with open('private/auth.json') as file_:
        splatoon_data = json.loads(file_.read())['splatoon']
        app_head = splatoon_data['headers']
        cookies = splatoon_data['cookies']

    url = f'{BASE_URL}/api/schedules'
    req = requests.get(url, headers=app_head, cookies=cookies)

    return req.json()


def combine_gamemodes(schedule):
    all_entries = []
    for gamemode in schedule.values():
        all_entries += gamemode

    return all_entries


def search_schedule(focus, *args):
    schedule = get_schedule()
    entries = [ScheduleItem(x) for x in combine_gamemodes(schedule)]
    filtered = list(sorted(filter(lambda x: focus(x) in args, entries), key=lambda x: x.start))
    return filtered


if __name__ == '__main__':
    # schedule = get_schedule()
    filtered = search_schedule(lambda x: x.ruleset[1], 'rainmaker')
    print('\n'.join(map(str, filtered)))

    # for entry in schedule['gachi']:
    #     print(ScheduleItem(entry))

