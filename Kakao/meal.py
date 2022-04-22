from datetime import datetime, timedelta
import requests
import json
import re


async def getMeal(when="오늘"):
    date = datetime.today()  # 오늘을 기준으로
    p = re.compile('^[0-9]{8}$')
    if when == "내일":
        date += timedelta(days=1)
    elif when == "모레":
        date += timedelta(days=2)
    elif p.match(when) is not None:
        year = int(when[0:4])
        month = int(when[4:6])
        day = int(when[6:])
        date = datetime(year, month, day)

    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    param = {
        "Type": "json",
        "ATPT_OFCDC_SC_CODE": "E10",
        "SD_SCHUL_CODE": "7310348",
        "MLSV_YMD": date.strftime("%Y%m%d"),  # YYYYmmdd
    }

    response = requests.get(url, param)
    json_obj = json.loads(response.text)
    try:
        meals = json_obj["mealServiceDietInfo"][1]['row'][0]['DDISH_NM'].split("<br/>")
    except KeyError:
        meals = False

    msg = "[인천고잔고등학교]  " + date.strftime("%Y-%m-%d") + "\n"
    msg += "🤔이 날의 맛점 메뉴는?🍙\n"
    msg += '------------------------------'

    if not meals:
        msg += "\n밥 안나와요...😭"
        msg += '\n------------------------------'
        msg += "\n그래도... 맛있게 먹어..💕"
    else:
        for menu in meals:
            msg += "\n•" + menu
    msg += '\n------------------------------'
    msg += "\n맛있게 먹어💕"

    return msg
