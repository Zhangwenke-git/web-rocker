import socket
import json
from utils.pubulic.logger import Logger
from utils.pubulic.ReadConfig import ReadConfig
logger = Logger("socket client")


def client(data):
    mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mysocket.connect(ReadConfig.getWebsocket())

    data = json.dumps(data)
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



