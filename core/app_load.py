from django import conf
from utils.pubulic.logger import Logger

logger = Logger("core app_load")


def app_loader(appname):
    for application in conf.settings.INSTALLED_APPS:
        try:
            mod = __import__("%s.%s_admin" % (application,appname))
            #logger.debug(f"Success to import application :[{application}]")
        except ImportError as e:
            pass
