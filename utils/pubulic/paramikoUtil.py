import paramiko
from utils.pubulic.logger import Logger

logger = Logger("myParamiko")


class MyParamiko:

    def __init__(self,linux_server_dict):
        self.hostip = linux_server_dict.get("hostname")
        self.port = linux_server_dict.get("port")
        self.username = linux_server_dict.get("username")
        self.password = linux_server_dict.get("password")
        self.obj = paramiko.SSHClient()
        self.obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.obj.connect(self.hostip, self.port, self.username, self.password)
        logger.info(
            f"Success to establish connection with linux server by [{self.hostip}|{self.port}|{self.username}|{self.password}]")
        self.objsftp = self.obj.open_sftp()

    def run_cmd(self, cmd):
        if len(cmd) != 0:
            stdin, stdout, stderr = self.obj.exec_command(cmd)
            logger.debug(f"Success to execute command : [{cmd}]")
            return stdout.read().decode("utf-8")
        else:
            logger.error(f"The command is blank string,nothing can be output!")

    def run_cmdlist(self, cmdlist):
        self.resultList = []
        for cmd in cmdlist:
            stdin, stdout, stderr = self.obj.exec_command(cmd)
            self.resultList.append(stdout.read())
        return self.resultList

    def get(self, remotepath, localpath):
        self.objsftp.get(remotepath, localpath)

    def put(self, localpath, remotepath):
        self.objsftp.put(localpath, remotepath)

    def getTarPackage(self, path):
        list = self.objsftp.listdir(path)
        for packageName in list:
            stdin, stdout, stderr = self.obj.exec_command("cd " + path + ";"
                                                          + "tar -zvcf /tmp/" + packageName
                                                          + ".tar.gz " + packageName)
            stdout.read()
            self.objsftp.get("/tmp/" + packageName + ".tar.gz", "/tmp/" + packageName + ".tar.gz")
            self.objsftp.remove("/tmp/" + packageName + ".tar.gz")
            print("get package from " + packageName + " ok......")

    def close(self):
        self.objsftp.close()
        self.obj.close()


if __name__ == '__main__':
    sshobj = MyParamiko({})
    text = sshobj.run_cmd("grep '200711050100000092' /home/tbs/app/tbs-dp-css/logs/css-debug.log")
    print(text, len(text), type(text))
    sshobj.close()
