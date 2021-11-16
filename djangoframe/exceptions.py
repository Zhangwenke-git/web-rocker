from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict


class BaseError(APIException):
    def __init__(self, detail=None, statue_code=status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = statue_code


class FailureResponse(BaseError):
    def __init__(self, code=-1, message="异常错误", success=False, result=None):
        if isinstance(message, ReturnDict):
            try:
                message = message
            except IndexError:
                pass
        detail = {
            "code": code,
            "message": message,
            "success": success,
            "result": result,
        }
        super(FailureResponse, self).__init__(detail)


class SuccessResponse(BaseError):
    def __init__(self, code=0, message="响应成功", success=True, result=None):
        detail = {
            "code": code,
            "message": message,
            "success": success,
            "result": result,
        }
        super(SuccessResponse, self).__init__(detail, statue_code=status.HTTP_200_OK)
