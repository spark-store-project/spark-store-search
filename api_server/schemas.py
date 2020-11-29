from typing import List
from pydantic import BaseModel

class ScreenshotItem(BaseModel):
    url: str

    class Config:
        orm_mode = True

class AppItem(BaseModel):
    id: int
    name: str
    version: str 
    path: str 
    pkgname: str 
    author: str 
    contributor: str 
    website: str 
    size: str 
    more: str 
    tags: str 
    icon: str 
    imgs: List[str] = []
    category_slug: str 

    class Config:
        orm_mode = True

