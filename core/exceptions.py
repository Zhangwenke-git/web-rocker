from rest_framework.exceptions import APIException
from rest_framework import status


class BaseError(APIException):
    """自定义异常基础类"""

    def __init__(self, detail=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code


class DefiendError(BaseError):
    """默认异常，自定义使用，返回状态-1，响应状态400"""

    def __init__(self, message="发生异常", code=-1, success=False, result=None):
        detail = {'code': code, 'message': message, 'success': success, 'result': result}
        super(DefiendError, self).__init__(detail)


class DefiendSuccess(BaseError):
    """默认异常，自定义使用，返回状态0，响应状态200"""

    def __init__(self, message="响应成功", code=0, success=True, result=None):
        detail = {'code': code, 'message': message, 'success': success, 'result': result}
        super(DefiendSuccess, self).__init__(detail,status_code=status.HTTP_200_OK)