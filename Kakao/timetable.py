import json
import os
import enum
import unicodedata

from wcwidth import wcswidth


def x(string, width, align='<', fill=' '):
    count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF")
                         for c in string))
    return {
        '>': lambda s: fill * count + s,
        '<': lambda s: s + fill * count,
        '^': lambda s: fill * (count / 2)
                       + s
                       + fill * (count / 2 + count % 2)
    }[align](string)


def preformat_cjk(x, w, align='l'):
    x = str(x)
    l = wcswidth(x)
    s = w - l
    if s <= 0:
        return x
    if align == 'l':
        return x + ' ' * s
    if align == 'c':
        sl = s // 2
        sr = s - sl
        return ' ' * sl + x + ' ' * sr
    return ' ' * s + x


class Day(enum.IntEnum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4


async def getTimetable(when="week"):
    with open(f'{os.path.dirname(os.path.abspath(__file__))}{os.sep}resources{os.sep}timetable.json', 'r',
              encoding='UTF-8') as f:
        table_json = json.loads(f.read())

    timetable = [["-"] * 5 for _ in range(7)]
    table_week = table_json["week"]

    if when == "week":
        for day in Day:
            table_day = table_week[day][day.name]
            for subject in table_day:
                timetable[int(subject["period"]) - 1][day] = subject["subject"]

        msg = "%s%s%s%s%s" % (preformat_cjk("월", 8), preformat_cjk("화", 8), preformat_cjk("수", 8),
                              preformat_cjk("목", 8), preformat_cjk("금", 8))
        msg += "\n"
        for period in timetable:
            msg += "%s%s%s%s%s" % (preformat_cjk(period[0], 8), preformat_cjk(period[1], 8),
                                   preformat_cjk(period[2], 8), preformat_cjk(period[3], 8),
                                   preformat_cjk(period[4], 8))
            msg += "\n"
        print(msg)
        return msg

    if when == "월":
        msg = ""
        table_monday = table_week[Day.Monday]["Monday"]

        for subject in table_monday:
            msg += "{0:^4}".format(subject["subject"])
            msg += "\n"
            msg += "{0:^4}".format('-')

        return msg
