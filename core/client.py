import socket
import json
from utils.pubulic.logger import Logger

logger = Logger("Websocket client")


def client(data):
    mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mysocket.connect(('127.0.0.1',5678))

    data = json.dumps(data,indent=4,ensure_ascii=False)
    data = data.encode(encoding='utf-8')
    flag,html = False,""
    mysocket.send(data)
    while True:
        result=mysocket.recv(1024)
        if result:
            result = result.decode(encoding='utf-8')
            flag,html = result.split("|")
            logger.info(f"The execution result is: [{result}]")
            if flag == "SUCCESS":
                flag=True
        else:
            break
    mysocket.close()
    return flag,html
