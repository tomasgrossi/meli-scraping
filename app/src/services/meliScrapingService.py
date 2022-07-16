from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

class MeliService():
    
    def __init__(self):
        pass
    
    
    
    clear_prices = lambda self, dirty_string: float(re.sub("[^0-9]", "", dirty_string)) if dirty_string != '' else None
    
    def scraping_offers(self):
        
        try:    
            client = urlopen('https://www.mercadolibre.com.ar/ofertas?container_id=MLA779357-1&page=2')
            
            page = client.read()
            
            client.close()
            
            
            soup = BeautifulSoup(page, 'html.parser')
            
            
            items = soup.findAll('div',{'class':'promotion-item__container'})
            
            list_objs = []
            
            for item in items:
                
                list_objs.append({
                    'offer_product_old_price' : self.clear_prices(item.find('span',{'class':'promotion-item__oldprice'}).text),
                    'offer_product_offer_price' : self.clear_prices(item.find('span',{'class':'promotion-item__price'}).span.text),
                    'offer_product_title' : item.find('p',{'class':'promotion-item__title'}).text,
                    'offer_product_img' : item.find('img',{'class':'promotion-item__img'}).attrs['src'],   
                })
                
                
        
            return list_objs
        
        except Exception as error:
            print(error)
            return 'Failure'
    
    
    