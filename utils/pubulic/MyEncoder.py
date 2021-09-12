import json
import datetime
import requests
from requests import structures
from utils.pubulic.logger import Logger

logger = Logger("DefaultEncoder")


class DefaultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if hasattr(obj, "DoesNotExist"): # 处理django中model对象
            return str(obj)
        if isinstance(obj,requests.structures.CaseInsensitiveDict):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)


def encoder_render(obj):
    if isinstance(obj, dict):
        try:
            obj_str = json.dumps(obj, cls=DefaultEncoder, indent=4, ensure_ascii=False)
            obj = json.loads(obj_str)
        except Exception as e:
            logger.error(f"Fail to transfer the object: [{obj}],error as follows:{str(e)}")

    elif isinstance(obj, str):
        try:
            obj_dict = json.loads(obj)
            obj = encoder_render(obj_dict)
        except Exception as e:
            logger.error(f"Fail to transfer the object: [{obj}],error as follows:{str(e)}")
    else:
        logger.error(f"Invalid parameter,only support string and dict type,not [{obj}]")
    return obj


if __name__ == "__main__":
    x = {'id': 5, 'name': '支付宝', 'description': '支付宝结算API接口', 'start': datetime.date(2021, 9, 16),
         'end': datetime.date(2021, 9, 3), 'statue': 1}

    y = encoder_render(x)
    print(y)
