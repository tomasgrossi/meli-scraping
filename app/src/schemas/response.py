from pydantic import BaseModel, Field
from typing import Optional, List
from ..models import MeliModel

class Meli(BaseModel):
    
    id: int
    title: str
    url: str
    img: str
    old_price: Optional[float]
    price: float
    scraping_at: int
    
    class Config:
        orm_mode = True

class Response(BaseModel):
    
    status_code: int
    message: str
    
    
class ResponseListMeliObj(Response):
    count:int
    limit:int
    offset:int
    data: List[Meli] = Field(...)
    