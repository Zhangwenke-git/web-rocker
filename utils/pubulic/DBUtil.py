import os
import cx_Oracle
import pymysql
from utils.pubulic.logger import Logger
from pymysql.cursors import DictCursor

logger = Logger('DBUtil')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class DBconnect(object):
    def __init__(self, dbinfo_dict, type="oracle", dict_flag=False):

        dbhost = dbinfo_dict.get("dbhost")
        dbport = dbinfo_dict.get("dbport")
        dbname = dbinfo_dict.get("dbname")
        username = dbinfo_dict.get("username")
        password = dbinfo_dict.get("password")

        if type.lower() == "oracle":
            self.param = username + "/" + password + "@" + dbhost + ":" + dbport + "/" + dbname
            self.conn = cx_Oracle.connect(self.param)

        elif type.lower() == "mysql":
            self.conn = pymysql.connect(user=username, password=password, host=dbhost, database=dbname,
                                        port=int(dbport), charset='utf8')
        else:
            raise NameError("仅支持oracle和mysql!")
        if dict_flag:
            self.cursor = self.conn.cursor(DictCursor)
        else:
            self.cursor = self.conn.cursor()
        logger.debug(f"Success to connect database [{dbinfo_dict}]!")

    def execute(self, sql):
        logger.debug(f"Prepare to execute sql: {sql}")
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
        logger.debug(f"Success to close database connection!")

    def query(self):
        data_list = self.cursor.fetchall()
        return data_list

    def output_selfdefined_dict(self, sql, param_dict=None, field_list=None, limit=None):

        if param_dict:
            if isinstance(param_dict, dict):
                sql = sql.format(**param_dict)
            elif isinstance(param_dict, str):
                sql = sql % param_dict
        self.execute(sql)
        data_list = []
        try:
            data_list = self.cursor.fetchall()
            if len(data_list) != 0:
                if limit and int(limit) < len(data_list):
                    data_list = data_list[:int(limit)]
                else:
                    logger.debug(f"Success to find: {len(data_list)} items,but you input limit is: {limit}")
                if field_list:
                    if isinstance(field_list, list) and len(field_list) != 0:
                        result_list = []
                        for item in data_list:
                            item_dic = {}
                            item = list(item)
                            if len(field_list) == len(item):
                                for index, temp in enumerate(item):
                                    item_dic[field_list[index]] = str(temp)
                                result_list.append(item_dic)
                                data_list = result_list
                            else:
                                logger.error(
                                    f"The length of fields list must be equal to the length of database fields!")
                                break
                    else:
                        logger.error(f"Fields list parameter must list type and can not be blank!")
                else:
                    data_list = [x[0] for x in data_list]
            else:
                logger.warning("There is no data in table!")
                data_list = [{}]
        except Exception:
            logger.error(f"Fail to query database!")
        return data_list


if __name__ == "__main__":
    pass
