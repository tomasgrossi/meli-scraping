from urllib.request import urlopen
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from app.src.utils.decorators import try_except
from ..models import MeliModel
from sqlalchemy.orm import Session
from ..schemas import Response, ResponseListMeliObj
import re
from ..utils import try_except
class MeliService():
    
    def __init__(self, session: Session):
        
        self.session = session
        
        self.list_objs = []
        
    clear_prices = lambda self, dirty_string: float(re.sub("[^0-9]", "", dirty_string)) if dirty_string != '' else None
    
    get_image = lambda self, img : img.attrs['data-src'] if img.attrs['src'].find("data:image/gif;base64") >= 0 else img['src']
    
    def __scraping_page(self, page):
        
        url = f'https://www.mercadolibre.com.ar/ofertas?container_id=MLA779357-1&page={page}'
                    
        client = urlopen(url)
    
        page = client.read()
        
        client.close()
    
        soup = BeautifulSoup(page, 'html.parser')
    
        items = soup.findAll('li',{'class':'promotion-item'})
        
        for item in items:
            
            dict_item = {
                'old_price' : self.clear_prices(item.find('span',{'class':'promotion-item__oldprice'}).text),
                'price' : self.clear_prices(item.find('span',{'class':'promotion-item__price'}).span.text),
                'title' : item.find('p',{'class':'promotion-item__title'}).text,
                'img' : self.get_image(item.find('img',{'class':'promotion-item__img'})), 
                'url' : item.find('a',{'class':'promotion-item__link-container'}).attrs['href'],     
            }
            
            self.list_objs.append(MeliModel(**dict_item))
    
    @try_except('Error to scraping meli offers')
    def scraping_offers(self):
        
            
        paginator_url = urlopen('https://www.mercadolibre.com.ar/ofertas#nav-header')
        
        paginator_page = paginator_url.read()
        
        paginator_url.close()
        
        paginator_soup = BeautifulSoup(paginator_page, 'html.parser')
        
        max_pages = int(paginator_soup.findAll('li',{'class':'andes-pagination__button'})[-2].text)
        
        with ThreadPoolExecutor() as executor:
            
            for page in range(1, max_pages+1):
                
                executor.submit(self.__scraping_page, page=page)
                
            
        
        self.session.bulk_save_objects(self.list_objs)
        self.session.commit()
        
        return Response(
            status_code=200,
            message=f'scraping ok, {len(self.list_objs)} new registries'
        )
        
    
    @try_except('Error to get meli offers')
    def get_offers(self, limit=0, offset=0, search=None):
        
        query = self.session.query(MeliModel)
        
        if search:
            query = query.filter(MeliModel.title.contains(search))
        
        if limit:
            query = query.limit(limit).offset(offset * limit)
            
            
        return ResponseListMeliObj(
            status_code=200,
            message='ok',
            count=query.count(),
            limit=limit,
            offset=offset,
            data=query.all()
        )