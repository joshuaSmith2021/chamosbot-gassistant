import datetime
import json

import requests

import tools

BASE_URL = 'https://app.splatoon2.nintendo.net'

with open('data/splatoon2/gamemodes.json') as file_:
    GAMEMODES = json.loads(file_.read())

with open('data/splatoon2/rulesets.json') as file_:
    RULESETS = json.loads(file_.read())

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

    def start_string(self):
        time_format = '%-I:%M%p'
        return f'{self.start.strftime(time_format)} {tools.get_today_tomorrow(self.start)}'

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


def stages_notification(blocks, include_gamemode=True, include_ruleset=False,
                        include_stage=False, include_time=True):
    with open('data/splatoon2/gamemodes.json') as file_:
        gamemodes = json.loads(file_.read())

    result = []

    for gamemode in gamemodes:
        current_blocks = [x for x in blocks if gamemode['id'] == x.gamemode[1]]

        if len(current_blocks) == 0:
            continue

        mode_result = []
        if include_gamemode:
            mode_result.append(gamemode['name'])

        for block in current_blocks:
            current_string = []
            if include_ruleset:
                current_string.append(block.ruleset[1])

            if include_stage:
                current_string.append(f"on {' and '.join(map(str, block.stages))}")

            if include_time:
                current_string.append(f'at {block.start_string()}')

            mode_result.append(' '.join(current_string))

        result.append(', '.join(mode_result))

    return '. '.join(result)


if __name__ == '__main__':
    # schedule = get_schedule()
    filtered = search_schedule(lambda x: x.ruleset[1], 'rainmaker')
    print(stages_notification(filtered))
    print('\n'.join(map(str, filtered)))

