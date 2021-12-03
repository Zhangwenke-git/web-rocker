import json
from rest_framework.exceptions import APIException
from rest_framework import status
from utils.pubulic.logger import Logger
from utils.pubulic.MyEncoder import encoder_render
logger = Logger("Exceptions")


class BaseError(APIException):
    """自定义异常基础类"""

    def __init__(self, detail=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code


class DefaultError(BaseError):
    """默认异常，自定义使用，返回状态-1，响应状态400"""

    def __init__(self, message="发生异常", code=-1, success=False, result=None):
        detail = {'code': code, 'message': message, 'success': success, 'result': result}
        super(DefaultError, self).__init__(detail)


class DefinedtError(BaseError):
    """默认异常，自定义使用，返回状态-1，响应状态200"""

    def __init__(self, message="发生错误", code=1, success=False, result=None):
        detail = {'code': code, 'message': message, 'success': success, 'result': result}
        super(DefinedtError, self).__init__(detail, status_code=status.HTTP_200_OK)
        if result:
            if result.get("data"):
                try:
                    result["data"] = encoder_render(result["data"])
                except Exception:
                    pass
        logger.debug(encoder_render(detail))


class DefinedSuccess(BaseError):
    """默认异常，自定义使用，返回状态0，响应状态200"""

    def __init__(self, message="响应成功", code=0, success=True, result=None):
        detail = {'code': code, 'message': message, 'success': success, 'result': result}
        super(DefinedSuccess, self).__init__(detail, status_code=status.HTTP_200_OK)
        if result:
            if result.get("data"):
                try:
                    result["data"] = encoder_render(result["data"])
                except Exception as e:
                    pass
        logger.debug(encoder_render(detail))
