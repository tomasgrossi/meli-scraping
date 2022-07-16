from .router import Router
from ..services import MeliService

@Router.get("/")
def root():
    return MeliService().scraping_offers()