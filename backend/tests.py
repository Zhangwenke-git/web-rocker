data = {
    "duringTime": 401,
    "timesPerDay": 10000,
    "device": {
        "appid": 1,
        "appName": "com.planet2345.com",
        "appName2": "com.planet2345.com2"
    },
    "user_list": [
        {
            "name": "zhangsan",
            "age": 12
        },
        {
            "name": "wenle",
            "age": 34
        },
        {
            "name": "wadqwdq",
            "age": 21
        }
    ]
}


class KeysAcquire():
    def __init__(self):

        self.key_list = []

    def get_dict_allkeys(self, dict_a):

        if isinstance(dict_a, dict):  # 使用isinstance检测数据类型

            for temp_key,temp_value in dict_a.items():
                self.key_list.append(temp_key)
                self.get_dict_allkeys(temp_value)  # 自我调用实现无限遍历

        elif isinstance(dict_a, list):
            _dict,_list = dict(),[]
            for k in dict_a:

                if isinstance(k, dict):

                    for x in range(len(k)):
                        temp_key = list(k.keys())[x]

                        temp_value = k[temp_key]

                        self.key_list.append(temp_key)

                        self.get_dict_allkeys(temp_value)

        return self.key_list

def get_json_value_by_key(in_json, target_key, results=[]):
    if isinstance(in_json, dict):  # 如果输入数据的格式为dict
        for key in in_json.keys():  # 循环获取key
            data = in_json[key]
            get_json_value_by_key(data, target_key, results=results)  # 回归当前key对于的value

            if key == target_key:  # 如果当前key与目标key相同就将当前key的value添加到输出列表
                results.append(data)

    elif isinstance(in_json, list) or isinstance(in_json, tuple):  # 如果输入数据格式为list或者tuple
        for data in in_json:  # 循环当前列表
            get_json_value_by_key(data, target_key, results=results)  # 回归列表的当前的元素

    return results

import json
import json2html

#infoFromJson = json.loads(data)




if __name__ == "__main__":
    s = KeysAcquire()
    keys = s.get_dict_allkeys(data)
    print(keys)

    data1 = {
  "url": "https://200.31.153.206/tbs_qt_css/odm/cbt",
  "method": "POST",
  "header": {"content-type": "application/json", "Authorization":"9480295ab2e2eddb8"},
  "validator": 200,
  "data": {
    "header": {
      "dplcF": 12,
      "erCd": "55",
      "erMsg": "rg",
      "lang": "yy",
      "msgSndngTm": "ss",
      "msgSrcEnd": 0,
      "msgUuid": "1947cccd-ee71-f89f-1a55-6ccfc041833a",
      "sesnId": "324372174923834258345",
      "sndrCmpntId": 102410,
      "sndrSubId": 30025,
      "tgtCmpntId": "111",
      "tgtSubId": "11",
      "tpcNm": "ee",
      "tstMdF": 22,
      "srvcId": 4091001
    },
    "ordrData": {
      "clntQtCd": "",
      "stlmntSpdNm": 2,
      "cntngncyIndctr": None,
      "flxblNetPrc": None,
      "trdAcntCnShrtNm": "{{instnNm}}",
      "qtTp": "5",
      "netPrc": "{{netPrc}}",
      "instnCd": "{{instnCd}}",
      "nmnlVol": "{{volumn}}",
      "ordrTpIndctr": "1",
      "trdrCd": "{{trdrCd}}",
      "dir": "{{dir}}",
      "traTlCd": "{{traTlCd}}",
      "bndsNm": "{{bndsNm}}",
      "userRefInfo": {
        "key": "1",
        "vl": "2"
      },
      "prdctCd": "CBT",
      "stlmntDt": "${today}|<>",
      "clrngMthd": 6,
      "isrCd": 100086,
      "qtSrc": "0",
      "trdngAcntCd": "{{trdAcountCd}}",
      "srNoId": 256,
      "trdAcntSrNo": 412,
      "dlrSqncNoId": 125,
      "instnSrno": 124,
      "ordrCd": "",
      "flxblSpd": "",
      "dtCnfrm": "${current}|<>",
      "alctnIndctr": 2
    },
    "cbtOrdrData": {
      "yldToMrty": 3.2541,
      "exrcsYld": None,
      "bondTpNm": 100004,
      "ttm": "1Y12D",
      "flxblExrcsYld": "",
      "flxblYldToMrty": "",
      "acrdIntrst": "1.254155",
      "prmrktBondF": "0"
    }
  }
}


    print(dir(json2html.json2html))
    print(json2html.json2html.convert(json=data))



    for key in keys:
        print(get_json_value_by_key(data, key))