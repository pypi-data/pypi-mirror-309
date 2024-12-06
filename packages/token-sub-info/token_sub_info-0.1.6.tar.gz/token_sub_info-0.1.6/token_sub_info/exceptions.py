from fastapi import status

from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from .schemas.schemas import ResponseDetail, ExceptionDetail


class ServiceException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = jsonable_encoder(
        ExceptionDetail(
            detail=ResponseDetail(
                code="OTHER_ERROR",
                message="Ошибка взаимодействия с библиотекой token_sub_info."
            )
        )
    )

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectTokenFormatException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = jsonable_encoder(
        ExceptionDetail(
            detail=ResponseDetail(
                code="TOKEN_INCORRECT",
                message="Неверный формат токена."
            )
        )
    )


class UserUnauthorizedException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = jsonable_encoder(
        ExceptionDetail(
            detail=ResponseDetail(
                code="UNAUTHORIZED",
                message="Пользователь не авторизован."
            )
        )
    )


class TokenExpiredException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = jsonable_encoder(
        ExceptionDetail(
            detail=ResponseDetail(
                code="TOKEN_EXPIRED",
                message="Токен истек."
            )
        )
    )


class AllOrganizationAccessForbiddenException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = jsonable_encoder(
        ExceptionDetail(
            detail=ResponseDetail(
                code="FORBIDDEN",
                message="Пользователь не имеет доступа ни к одной из организаций."
            )
        )
    )
