from fastapi import FastAPI
import enum

from Kakao import meal, timetable

app = FastAPI()

'''
 * (string) room
 * (string) sender
 * (boolean) isGroupChat
 * (void) replier.reply(message)
 * (boolean) replier.reply(room, message, hideErrorToast = false) // 전송 성공시 true, 실패시 false 반환
 * (string) imageDB.getProfileBase64()
 * (string) packageName
'''


class ResponseCode(enum.IntEnum):
    OK = 200
    CommandError = 100
    ArgumentError = 110


@app.get("/kakao")
async def kakao(room: str, msg: str, sender: str, isGroupChat: bool, replier, imageDB: str, packageName: str):
    msg = msg.split(" ", 1)
    command = msg[0]
    hasArg = True if "".join(msg[1:]) != "" else False
    result = {
        "code": ResponseCode.CommandError,
        "msg": "알 수 없는 명령어 :(",
    }
    if command == "급식":
        print("".join(msg[1:]))
        result["code"] = ResponseCode.OK
        result["msg"] = await meal.getMeal("".join(msg[1:]) if hasArg else None)
    if command == "시간표":
        result["code"] = ResponseCode.OK
        result["msg"] = await timetable.getTimetable("".join(msg[1:]) if hasArg else None)

    return result

# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
