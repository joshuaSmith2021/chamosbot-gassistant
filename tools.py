def english_list(_list):
    _list = [str(x) for x in _list]
    if len(_list) == 0:
        return ''
    elif len(_list) == 1:
        return _list[0]
    else:
        body = ', '.join(_list[:-1])
        result = f'{body}, and {_list[-1]}'
        return result


def get_online(player):
    return (player.is_online(), player.alias)


if __name__ == '__main__':
    print(english_list(['wow', 5, None]))
    # outputs "wow, 5, and None"

