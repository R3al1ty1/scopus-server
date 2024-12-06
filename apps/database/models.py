from pydantic import BaseModel


class SPub(BaseModel):
    filters_dct: dict
    folder_id: str
    verification: str


class SAuth(BaseModel):
    filters_dct: dict
    folder_id: str
    search_type: str
    verification: str


class SAuthInfo(BaseModel):
    folder_id: str
    author_id: str
    verification: str
