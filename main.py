from fastapi import FastAPI
import enum

from Kakao import meal

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
    result = {
        "code": ResponseCode.CommandError,
        "msg": "알 수 없는 명령어 :(",
    }
    if command == "급식":
        print("".join(msg[1:]))
        result["code"] = ResponseCode.OK
        result["msg"] = await meal.getMeal("".join(msg[1:]))

    print(f'{room, msg, sender, isGroupChat, replier, imageDB, packageName}')
    return result

# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
