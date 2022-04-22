from fastapi import FastAPI
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


@app.get("Kakao")
async def kakao(room: str, msg: str, sender: str, isGroupChat: bool, replier, imageDB: str, packageName: str):
    msg = msg.split(" ", 1)
    command = msg[0]
    result = "알 수 없는 명령어 :("
    if command == "급식":
        print("".join(msg[1:]))
        result = await meal.getMeal("".join(msg[1:]))

    print(f'{room, msg, sender, isGroupChat, replier, imageDB, packageName}')
    return {"result": result}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


