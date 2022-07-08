from rest_framework.permissions import BasePermission
from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status

# BasePermission 상속 필수!
class isCandidateUser(BasePermission):
    # False 리턴 시 보여주는 메세지
    message = '구직자만 지원할 수 있습니다.'

    # has_permission 오버라이딩
    def has_permission(self, request, view):
        user = request.user
        # 가입 후 3분이 지난 사용자만 허가 ex) 글쓰기 권한
        elif request.method == "POST" and 
        	user.user_type == "candidate":
                return True
        # admin의 경우 허가
        elif user.is_admin:
            return True
        
        return False

# is_authenticated 값이 없을 경우 발생 시킬 예외 정의
class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)

class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    # 메서드 지정을 통해서도 세부적인 권한 조절 가능
    SAFE_METHODS = ('GET', )
    # return 값 False 일 때 전달할 메세지
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        # 먼저 로그인 되어있지 않은 것을 판별해서 예외 처리해야만한다 하지않을 경우
        # 로그인되어있지 않다는 오류가 메세지로 나오고 접근 권한에 대해서는 판별도 되지 않게 됨
        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        # 로그인 ok, admin ok
        if user.is_authenticated and user.is_admin:
            return True
        # 로그인 ok, method==GET ok, 
        elif user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        
        return False