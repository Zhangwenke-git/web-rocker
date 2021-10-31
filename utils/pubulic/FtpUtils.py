import os
from datetime import datetime
from ftplib import FTP
from utils.pubulic.logger import Logger
from utils.pubulic.ReadConfig import ReadConfig

logger = Logger("FTP")


class FTPHelper(object):

    def __init__(self, ip, username, password, port=21, bufsize=1024, obj=None):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.bufsize = bufsize
        self.obj = obj

        ftp = FTP()
        ftp.connect(self.ip, self.port)
        try:
            ftp.login(self.username, self.password)
        except Exception as e:
            logger.error(f"Fail to login [{self.ip, self.port}] with user info [{self.username, self.password}]")
        else:
            logger.info(ftp.getwelcome())
            self.obj = ftp
            self.obj.set_debuglevel(0)

    def close(self):
        self.obj.quit()

    def create_dir(self, target_dir, remote_path="/data/report"):
        remote_path = os.path.join(remote_path, target_dir)
        remote_path = remote_path.replace('\\', '/')

        try:
            self.obj.mkd(remote_path)
        except:
            logger.debug('dir: %s already exists' % remote_path)
        else:
            logger.debug(f"Success to create dir [{remote_path}]")

    def upload_folder(self, local_path='../', remote_path='/data/report'):
        try:
            local_path = local_path.strip()
            local_path = local_path.rstrip('/')
            local_path = local_path.rstrip('\\')
            remote_path = remote_path.strip()
            remote_path = remote_path.rstrip('/')
            remote_path = remote_path.rstrip('\\')
            last_dir = os.path.basename(local_path)

            remote_path = os.path.join(remote_path, last_dir)
            remote_path = remote_path.replace('\\', '/')

            try:
                self.obj.mkd(remote_path)
            except Exception as e:
                logger.debug('dir: %s already exists' % last_dir)

            sub_items = os.listdir(local_path)
            for sub_item in sub_items:
                sub_item_path = os.path.join(local_path, sub_item)
                if os.path.isdir(sub_item_path):
                    self.upload_folder(sub_item_path, remote_path)
                else:
                    self.upload_file(sub_item_path, remote_path)
        except Exception as e:
            logger.error(f"Fail to upload folder to FTP server!")

    def upload_file(self, src_file_path, remote_path):
        remote_file_name = os.path.split(src_file_path)[1]
        remote_path = remote_path + '/' + remote_file_name
        try:
            if self.obj.size(remote_path) != None:
                logger.debug("File [%s] has already exist!" % remote_path)
        except Exception:
            pass

        with open(src_file_path, 'rb') as file_handler:
            self.obj.storbinary('STOR %s' % remote_path, file_handler)
            logger.info('file [%s] has been upload to ftp server successfully!' % src_file_path)

    def download_dir(self, local_path, remote_path):
        local_path = local_path.strip()
        remote_path = remote_path.strip()
        remote_path = remote_path.rstrip('/')
        remote_path = remote_path.rstrip('\\')

        last_dir = os.path.basename(remote_path)
        local_path = os.path.join(local_path, last_dir)
        local_path = local_path.replace('/', '\\')
        if not os.path.isdir(local_path):
            os.makedirs(local_path)

        sub_items = self.obj.nlst(remote_path)
        for sub_item in sub_items:
            try:
                self.obj.cwd(sub_item)
                self.download_dir(local_path, sub_item)
            except Exception:
                self.download_file(local_path, sub_item)

    def download_file(self, local_path, remote_file_path):
        last_file_name = os.path.split(remote_file_path)[1]
        local_file_path = os.path.join(local_path, last_file_name)

        if os.path.isfile(local_file_path):
            local_file_path = local_file_path.replace('\\', '/')
            logger.debug('File [%s] has already exist!' % local_file_path)

        with open(local_file_path, 'wb') as file_handle:
            self.obj.retrbinary('RETR %s' % remote_file_path, file_handle.write)
