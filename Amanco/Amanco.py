# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse



class AmancoSpider(scrapy.Spider):
    name = 'Amanco'
    allowed_domains = ['amanco.com.br']
    start_urls = ['http://amanco.com.br/produtos']

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='/Users/Bruno.cunha/PycharmProjects/untitled/geckodriver')

    def parse(self, response):
            links_categorys = [x for x in response.css('div.row a ::attr(href)').getall() if 'produtos' in x and 'produtos-amanco' not in x]
            for link in links_categorys:
                yield response.follow(link,self.selenium_category)
                
    
    def selenium_category(self,response):
        self.driver.get(response.url)
        page = self.driver.page_source
        search_button = True
        while search_button:
            try:
                button = self.driver.find_element_by_xpath('/html/body/main/article[3]/div/div/div[3]/div')
                button.click()
                print('clickei no botão')
            except:
                search_button = False
                print('nao encontrei')
        page = self.driver.page_source
        resp = HtmlResponse(url=response.url, body=page,encoding = 'utf-8')
        url_products = resp.css('div.row article.product a ::attr(href)').getall()

        print('links de produtos',url_products)
        
        

        for link in url_products:
            
            yield response.follow(link,self.parse_product)
    
    def parse_product(self,response):
        sobre = response.xpath('/html/body/main/article[2]/div/div[2]/div/div//text()').getall()
        titulo = response.xpath('/html/body/main/article[1]/div/div/h1//text()').get()
        caracteristicas = response.xpath('/html/body/main/article[2]/div/div[3]/div[1]/ul/li//text()').getall() 
        vantagens = response.xpath('/html/body/main/article[2]/div/div[3]/div[2]/ul/li//text()').getall()  
        categoria = response.url.replace('http://amanco.com.br/','').replace('/','|')  

        total_image = response.css('div.image').get()
        image = total_image[total_image.find('http'):total_image.find(')"')] 

        keys = [x for x in response.xpath('/html/body/main/article[3]/div/div/div[1]/div//text()').getall() if 'Quantidade' not in x]
        values = [x for x in response.css('div.product-items-rows div.product-item-row div.product-item-col ::text').getall() if x not in keys and 'Quantidade' not in x]
        rows = int(len(values)/len(keys))

        f = str()
        for i in range (0,rows):
            for j in range(0,len(keys)):
                f = f + keys[j]+': '+values[j+(len(keys)*i)]+' | '
        
        especificacoes = f 

        yield {'titulo':titulo,
               'especificacoes':especificacoes,
               'categoria':categoria,
               'caracteristicas':caracteristicas,
               'vantagens':vantagens,
               'sobre o produto':sobre,
               'imagem':image,
               'link':response.url}





        


        
