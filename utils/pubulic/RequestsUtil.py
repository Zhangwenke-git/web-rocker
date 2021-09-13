from utils.pubulic.logger import Logger
from utils.pubulic.Ua import *
from retrying import retry
import requests
import cchardet
import json
logger = Logger("requests")


@retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
def _request(url, method, headers=None, data=None,params_type=None,timeout=None, binary=False, **kwargs):
    logger.info("Start to request: {}".format(url))
    _header = {"User-Agent": ua()}
    _maxTimeout = timeout if timeout else 5
    _headers = headers if headers else _header
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = eval(data)
    logger.debug(f"""Request parameter are as follows:
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
<<<<<<< Updated upstream
=======
                #content = json.dumps(content, indent=4, ensure_ascii=False)
>>>>>>> Stashed changes
            except Exception:
                content = response.content if binary else response.content.decode(encoding)

            response_dict.update(
                {
                    "url": response.url,
                    "method": response.request.method,
                    "request_headers": json.loads(json.dumps(dict(response.request.headers))),
                    "request_body": data,
                    "params_type": params_type,
                    "duration":response.elapsed.total_seconds(),
<<<<<<< Updated upstream
                    "code":response.status_code,
                    "response_headers":json.loads(json.dumps(dict(response.headers))),
                    "response_body":content,

=======
                    "code":200,
                    #"request_headers": response.request.headers,
                    "response_headers": response.headers,
                    "method": method,
                    "url": response.request.url,
>>>>>>> Stashed changes
                 }
            )
        else:
            response_dict.update(
                {
<<<<<<< Updated upstream
                    "url": response.url,
                    "method": response.request.method,
                    "request_headers": json.loads(json.dumps(dict(response.request.headers))),
                    "request_body": data,
                    "params_type": params_type,
                    "duration":response.elapsed.total_seconds(),
                    "code":response.status_code,
                    "response_headers":json.loads(json.dumps(dict(response.headers))),
                    "response_body":response.text,

                 }
=======
                    "content": response.text,
                    "duration": response.elapsed.total_seconds(),
                    "code": response.status_code,
                    # "request_headers":response.request.headers,
                    # "response_headers":response.headers,
                    # "method":method,
                    # "url":response.request.url,

                }
>>>>>>> Stashed changes
            )

    except Exception as e:
        logger.error("Error occurred while requesting {url}, Msg: {e}".format(url=url, e=str(e)))
    logger.debug(f"""Response are as follows:
    {json.dumps(response_dict,indent=4,ensure_ascii=False,separators=(',',';'))}
    """)
    return json.dumps(response_dict)


if __name__ == "__main__":
<<<<<<< Updated upstream
    _request(url="https://piaofang.maoyan.com/dashboard-ajax?orderType=0&uuid=81815fdf-a369-49f2-96da-3ed240f43493", method="GET")
=======
    print(myrequest(url="https://piaofang.maoyan.com/dashboard/webHeatData?showDate=20210908&uuid=179cbc33ee7c8-0d0c55fd6df147-3f356b-e1000-179cbc33ee8c8", method="GET"))
>>>>>>> Stashed changes
