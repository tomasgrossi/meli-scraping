from sqlalchemy.schema import Column
from ..utils.connection import Base
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import Sequence
import time

REGISTRY_ID_SEQ = Sequence('registry_id_seq')

class MeliModel(Base):
    __tablename__ = 'meli_offers'
    
    id = Column(
        Integer,
        primary_key = True,
        unique = True,
        index = True,
        nullable=False,
        autoincrement=True
    )
    title = Column(String)
    old_price = Column(Float)
    price = Column(Float)
    img = Column(String)
    url = Column(String)
    scraping_at = Column(Integer, default=time.time())
    
    