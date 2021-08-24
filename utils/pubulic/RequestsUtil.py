from utils.pubulic.logger import Logger
from utils.pubulic.Ua import *
from retrying import retry
import requests
import cchardet
import json
logger = Logger("requests")


@retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
def myrequest(url, method, headers=None, data=None,params_type="FORM",timeout=None, binary=False, **kwargs):
    logger.info("Scraping: {}".format(url))
    _header = {"User-Agent": ua()}
    _maxTimeout = timeout if timeout else 5
    _headers = headers if headers else _header
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = eval(data)
    logger.debug(f"""
        Request parameter are as follows::
            url:{url},
            method:{method},
            headers:{headers},
            data:{data},
            params_type:{params_type},
            timeout:{timeout},
            binary:{binary},
    """)
    response_dict = {
        "content":None,
        "code":None,
        "duration":None
    }
    try:
        if method.lower() == "get":
            response = requests.request(method=method, url=url,headers=_headers,params=data, **kwargs)
        elif method.lower() == "post":
            if params_type.lower() == 'form':  # 发送表单数据，使用data参数传递
                response = requests.request(method=method, url=url, headers=_headers,data=data, **kwargs)
            elif params_type.lower() == 'json':  # 如果接口支持application/json类型，则使用json参数传递
                _headers.update({"Content-Type":"application/json"})
                response = requests.request(method=method, url=url,headers=_headers, json=data, **kwargs)
            else:  # 如果接口需要传递其他类型的数据比如 上传文件，调用下面的请求方法
                response = requests.request(method=method, url=url,headers=_headers, **kwargs)
        else:
            logger.error(f"Only POST and GET method can be supported!")
            response = None
        encoding = cchardet.detect(response.content)["encoding"]

        if response.status_code == 200:
            try:
                content = response.json()
                content = json.dumps(content, indent=4, ensure_ascii=False)
            except Exception:
                content = response.content if binary else response.content.decode(encoding)
            response_dict.update(

                {
                    "content":content,
                    "duration":response.elapsed.total_seconds(),
                    "code":200
                 }
            )
        else:
            response_dict.update(
                {
                    "content": response.text,
                    "duration": response.elapsed.total_seconds(),
                    "code": response.status_code
                }
            )
    except Exception as e:
        logger.error("Error occurred while scraping {url}, Msg: {e}".format(url=url, e=e))
    logger.debug(f"""
        Response are as follows:
            {response_dict}
    """)
    return response_dict


if __name__ == "__main__":
    print(myrequest(url="http://www.baidu.com", method="GET"))
