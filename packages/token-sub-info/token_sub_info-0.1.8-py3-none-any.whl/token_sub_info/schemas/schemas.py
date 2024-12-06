from pydantic import BaseModel


class ResponseDetail(BaseModel):
    code: str | None = None
    message: str | None = None


class ExceptionDetail(BaseModel):
    detail: ResponseDetail
