import datetime

def english_list(_list):
    _list = [str(x) for x in _list]
    if len(_list) == 0:
        return ''
    elif len(_list) == 1:
        return _list[0]
    elif len(_list) == 2:
        return ' and '.join(_list)
    else:
        body = ', '.join(_list[:-1])
        result = f'{body}, and {_list[-1]}'
        return result


def get_online(player):
    return (player.is_online(), player.alias)


def get_today_tomorrow(date):
    one_day = datetime.timedelta(1)
    now = datetime.datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + one_day
    two_days = tomorrow + one_day

    if date >= today and date < tomorrow:
        return 'today'
    elif date >= tomorrow and date < two_days:
        return 'tomorrow'
    elif date >= two_days:
        return date.strftime('on %B %-d')


if __name__ == '__main__':
    now = datetime.datetime.now()
    print(get_today_tomorrow(now))
    print(english_list(['wow', 5, None]))
    # outputs "wow, 5, and None"

