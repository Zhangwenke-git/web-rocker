from utils.pubulic.StringUtil import StringUtil
from utils.pubulic import logger
from functools import reduce
from utils.pubulic.DataUtil import DataUtil
from utils.compare.CN_fields_map import projectFieldMapDict
from utils.pubulic.Constant import Constant
from utils.pubulic.Assertion import Assertion
from utils.compare.FieldReflection import FieldReflect
from utils.compare.MappingConfig import mapping_dict

logger = logger.Logger("DictUtils")

assert_obj = Assertion()


class DictUtils(object):

    def _compare_dict(self, expected_dict, actual_dict):
        """
        :function:将两个字典公有的字段，取出value进行比较
        :param expected_dict:
        :param actual_dict:
        :return:
        """
        public_key = self._getPublicKeys(expected_dict, actual_dict)
        expected_list = []
        actual_list = []
        flag_list = []

        for key in public_key:
            if StringUtil.remove_spechart(expected_dict[key]) == StringUtil.remove_spechart(actual_dict[key]):
                flag = Constant.success_flag
            else:
                flag = Constant.fail_flag

            expected_list.append(expected_dict[key])
            actual_list.append(actual_dict[key])
            flag_list.append(flag)

        return public_key, expected_list, actual_list, flag_list

    def _compare_map_dict(self, expected_dict, actual_dict):
        """
        :function:将两个字典公有的字段，取出value进行比较,且返回英文对应的中文名称
        :param expected_dict:
        :param actual_dict:
        :return:
        """
        public_key = self._getPublicKeys(expected_dict, actual_dict)
        field_cn, expected_list, actual_list, flag_list = [], [], [], []

        for key in public_key:
            if StringUtil.remove_spechart(expected_dict[key]) == StringUtil.remove_spechart(actual_dict[key]):
                flag = Constant.success_flag
            else:
                flag = Constant.fail_flag

            expected_list.append(expected_dict[key])
            actual_list.append(actual_dict[key])
            flag_list.append(flag)

        for field in public_key:
            key_list = list(projectFieldMapDict.keys())
            if field in key_list:
                if projectFieldMapDict[field] == "":
                    rel = "名称配置为空"
                else:
                    rel = projectFieldMapDict[field]
            else:
                rel = "未找到中文名称"
            field_cn.append(rel)
        return public_key, field_cn, expected_list, actual_list, flag_list

    def _getPublicKeys(self, dict1, dict2):
        """
        :function:获取两个字典相同同的key作为list返回
        :param dict1:
        :param dict2:
        :return:list
        """
        public_keys = list(dict1.keys() & dict2.keys())
        # lambda dicts,dict2:list(dict1.keys() & dict2.keys())
        logger.debug(f"The public key list is :{public_keys}")
        return public_keys


    def _getmultikey(self, data_list):
        """
        :function: 获取[dict1,dict2,dict3....]中共有的key，并返回一个key_list,里面没有添加字段映射方法
        :param data_list:
        :return: list
        """
        public_key_list = []
        try:
            public_key_list = list(reduce(lambda a, b: a & b, map(dict.keys, data_list)))
        except Exception as e:
            logger.error(f"Fail to get public keys from the multiple dict,error as follows: {e}")
        else:
            logger.debug(f"The public keys is: {public_key_list}")
        return public_key_list

    def _getDistinctKeys(self, dict1, dict2):
        """
        :function:获取两个字典不同的key作为list返回
        :param dict1:
        :param dict2:
        :return:
        """
        distrnctKey = list(dict1.keys() ^ dict2.keys())
        # lambda dict1,dict2:list(dict1.keys() ^ dict2.keys())
        logger.debug(f"The distinct key list is :{distrnctKey}")
        return distrnctKey

    def _getmulti_distinctkey(self, data_list):
        """
        :function: 获取[dict1,dict2,dict3....]中非共有的key，并返回一个key_list,里面没有添加字段映射方法
        :param data_list:
        :return: list
        """
        distinct_key_list = []
        try:
            total_key_list = list(reduce(lambda a, b: a ^ b, map(dict.keys, data_list)))
        except Exception as e:
            logger.error(f"Fail to get distinct keys from the multiple dict,error as follows: {e}")
        else:
            public_keys_list = self._getmultikey(data_list)
            distinct_key_list = list(set(total_key_list)-set(public_keys_list))
        return distinct_key_list

    def _mergeDict(self, dict1, dict2):
        """
        :function:将两个字典重新组合成一个
        :param dict1:
        :param dict2:
        :return:
        """
        dictMerged = dict1.copy()
        dictMerged.update(dict2)
        return dictMerged

    def _multiDictMerge(self, dictList):
        """
        :function:将多个字典融合，融合过程是一个迭代的过程，dict1和dict2融合为一个新的dict1_2,dict1_2再与dict3融合，生成最终的一个dict
        :param dictList: {dict1,dict2,dict3},reduce为python的高阶函数，效果就逐层迭代，返回最终迭代的结果
        :return:
        """
        newDict = reduce(self._mergeDict, dictList)
        return newDict

    def _sortDictByKey(self, dic):
        """
        :function:将字典重新按照key进行排序返回
        :param dict0:
        :return:
        """
        sortDict = {}
        ziplist = sorted(zip(dic.keys(), dic.values()))
        for item_tuple in ziplist:
            sortDict[item_tuple[0]] = item_tuple[1]
        return sortDict

    def _sortDictByValue(self, dic):
        """
        :function:将字典重新按照value进行排序返回
        :param dict0: value中不能有int类型，需要为字符串
        :return:
        """
        sortDict = {}
        ziplist = sorted(zip(dic.values(), dic.keys()))
        print(ziplist)
        for item_tuple in ziplist:
            sortDict[item_tuple[1]] = item_tuple[0]
        return sortDict

    def test_func(self, param):
        """
        :function:返回为字符串类型的param,配合filter使用
        :param param:
        :return:
        """
        return type(param) == str

    def dictValidateMult(self, string, dic_list, number=1):
        """
        :function:判断一个字符串是否存在dic_list中，并取出前面number的dic
        :param string:
        :param dic_list: [dict1,dict2,dict3....]
        :param number: 取出string所在的dict，取出前几个
        :return:
        """
        flag = False
        target_dict_list = []
        try:
            for dict_item in dic_list:
                for key, value in dict_item.items():
                    if value == string:
                        target_dict_list.append(dict_item)
                if len(target_dict_list) == int(number):
                    flag = True
                    break
            if len(target_dict_list) < int(number) and len(target_dict_list) != 0:
                logger.debug(f"Only {len(target_dict_list)} dicts which correspond to the given condition!")
                flag = True
            elif len(target_dict_list) == 0:
                logger.debug(f"There is no dict which correspond to the given condition!")

        except Exception as e:
            logger.error(f"Fail to validate the {string} whether exists in dic_list,error as follow :{e}!")
        finally:
            if flag:
                logger.debug(f"The result is [{flag}],and the {string} in the list {target_dict_list}!")
            else:
                logger.error(f"The [{string}] is not in the dic_list!")
            return flag, target_dict_list



    def multcompare(self, dict_list, black_list=None, skipped_list=None):
        """
        :function: 对比一个[dict0,dict1,dict2,dict3....]数据，将dict0作为对比参照物，其余的dict1,dict2，dict3同字段的值对比，相同则通过
        :param dict_list:
        :return: [True,False,True....]
        """
        result_list = []
        logger.debug(f"Prepare to compare {len(dict_list)} sets of data: {dict_list}")
        blist = dict_list.copy()
        if len(blist) > 2:
            blist.pop(0)
            logger.debug(f"First column as expected result!")
        mapping_obj = FieldReflect(mapping_dict)
        public_key = mapping_obj.getReflect(dict_list)

        if len(public_key) != 0:
            if black_list and len(black_list) != 0:
                if len(black_list) <= len(public_key):
                    for black in black_list:
                        try:
                            public_key.remove(black)
                        except ValueError:
                            pass
                else:
                    raise NameError('Black list can not be longer than the public key!')

        logger.debug(f"The count of public keys is [{len(public_key)}] and content is : {public_key}")

        for key in public_key:
            pass_list = []
            for item_dict in blist:
                res = []
                if key in mapping_dict.keys():
                    for i in mapping_dict[key]:
                        res.append(item_dict.get(i))
                if not skipped_list:
                    if str(dict_list[0][key]) == str(item_dict.get(key)) or str(dict_list[0][key]) in res:
                        pass_list.append("passed")  # 1代表passed，0代表failed，2代表skipped
                    else:
                        pass_list.append("failed")
                else:
                    if key in skipped_list:
                        pass_list.append("skipped")
                    else:
                        if str(dict_list[0][key]) == str(item_dict.get(key)) or str(dict_list[0][key]) in res:
                            pass_list.append("passed")  # 1代表passed，0代表failed，2代表skipped
                        else:
                            pass_list.append("failed")

            result_list.append(assert_obj._aseertPFS(pass_list))

        pass_count = result_list.count("passed")
        skip_count = result_list.count("skipped")
        failed_count = result_list.count("failed")
        total_count = len(result_list)
        passinfo = [total_count, pass_count,failed_count,skip_count]
        return public_key, result_list, passinfo

    def tryCompare(self, dict_list, dict1, dict2, field):
        if isinstance(dict1, dict) and isinstance(dict2, dict) and isinstance(dict_list, list):
            if dict1.get(field) and dict2.get(field):
                if str(dict1[field]) != str(dict2[field]):
                    dict_list.reverse()
                else:
                    pass
            else:
                pass
        else:
            pass


if __name__ == "__main__":
    sample = DictUtils()
    dict1 = {"name": "zwk", "age": "45", "hobby": "music", "site": 'Beijing', "company": "AliBaBa"}
    dict2 = {"name": "lili", "age": "34", "hobby": "music", "site": 'Beijing', "company": "Tencent"}
    dict3 = {"name": "li453", "age": "56", "hobby": "music"}

    lists = ["12", 332, "32424", "rwerwer"]
    dic_list = [dict1, dict2, dict3]

    dictlist = [dict1, dict2, dict3]

    print(sample._sortDictByValue(dict1))

    print(sample._multiDictMerge(dictlist))

    x, y, m, n = sample._compare_dict(dict1, dict2)
    a, b, c, d, e = sample._compare_map_dict(dict1, dict2)

    # htmlobj = GenerateCompareReport()

    # htmlobj._generateENHtml(x, y, m, n, "en_compare_test")
    # htmlobj._generateCNHtml(a, b, c, d, e, "cn_compare_test")

    # a = lambda dict1, dict2: list(dict1.keys() ^ dict2.keys())
    # print(a(dict1, dict3))
    #
    # print(list(filter(sample.test_func, lists)))
    #
    # print(sample.dictValidateMult('music1', dic_list, number=5))
    #
    #print("-------", sample._getmultikey(dic_list))

    _list = [{"name": "li453", "age": "56", "hobby": "music"},{"name1": "li453", "age": "56", "hobby": "music"},{"name3": "li453", "age": "56", "hobby": "music"}]

    print("-------", sample._getmulti_distinctkey(dictlist))
