from .router import Router
from ..services import MeliService
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Depends
from ..utils.connection import get_connection
from ..schemas import Response, ResponseListMeliObj

@Router.get("/meli_scraping_offers", response_model=Response)
def meli_scraping_offers(session: Session = Depends(get_connection), credential:int = None):
    if credential == 1599:
        return MeliService(session=session).scraping_offers()
    return None

@Router.get("/get_offers", response_model=ResponseListMeliObj)
def get_offers(session: Session = Depends(get_connection), limit:Optional[int]=0, offset:Optional[int]=0, search:Optional[str]=None):
    return MeliService(session=session).get_offers(limit=limit, offset=offset, search=search)