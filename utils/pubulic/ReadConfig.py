import configparser
from config.path_config import conf_path

web_config = configparser.ConfigParser()
web_config.read(conf_path)


class ReadConfig:


    @staticmethod
    def getWebsocket():
        ip = web_config.get("websocket", "ip")
        port = web_config.get("websocket", "port")
        return ip,int(port)

    @staticmethod
    def getFtp():
        ip=web_config.get("ftp","ip")
        port=web_config.get("ftp","port")
        username=web_config.get("ftp","username")
        password=web_config.get("ftp","password")
        return (ip,int(port),username,password)